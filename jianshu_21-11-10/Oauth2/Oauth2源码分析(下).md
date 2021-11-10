# 二、密码模式源码

## 2.1 概述

访问`/oauth/token`会经过拦截器的顺序`ClientCredentialsTokenEndpointFilter`和`BasicAuthenticationFilter`，`ClientCredentialsTokenEndpointFilter`从request parameters中抽取client信息**(username，password，grant_type，client_id，client_secret)**，`BasicAuthenticationFilter`从header Authorization Basic XXXX中抽取client信息**(client_id和client_secret)**。



**流程：**

`TokenRequest`包含了基本信息`clientId,scope,requestParameters,grantType`等。根据`tokenRequest`获取`OAuth2Request`，初始化获得`OAuth2Authentication`，再去数据库里找`oauth2accesstoken`，如果有则直接返回，如果没有则创建新的`oauth2accesstoken`，并且和`OAuth2Authentication`一起存入数据库中。



## 2.2 源码

**摘要：**

- 四大角色：ResouceServer AuthorizationServer client user
- OAuth2AccessToken OAuth2Authentiaction
- OAuth2Request TokenRequest AuthorizationRequest
- TokenGranter TokenStore TokenExtractor DefaultTokenServices RemoteTokenServices
- ResourceServerConfigurerAdapter AuthorizationServerConfigurerAdapter
- TokenEndPoint(/oauth/token) AuthorizationEndPoint(/oauth/authorize) CheckTokenEndpoint(/oauth/check_token)



**TokenEndpoint类中定义了/oauth/token接口**

```java
@FrameworkEndpoint
public class TokenEndpoint extends AbstractEndpoint {

    private OAuth2RequestValidator oAuth2RequestValidator = new DefaultOAuth2RequestValidator();

    private Set<HttpMethod> allowedRequestMethods = new HashSet<HttpMethod>(Arrays.asList(HttpMethod.POST));

    @RequestMapping(value = "/oauth/token", method=RequestMethod.GET)
    public ResponseEntity<OAuth2AccessToken> getAccessToken(Principal principal, @RequestParam
    Map<String, String> parameters) throws HttpRequestMethodNotSupportedException {
        if (!allowedRequestMethods.contains(HttpMethod.GET)) {
            throw new HttpRequestMethodNotSupportedException("GET");
        }
        return postAccessToken(principal, parameters);
    }
    
    @RequestMapping(value = "/oauth/token", method=RequestMethod.POST)
    public ResponseEntity<OAuth2AccessToken> postAccessToken(Principal principal, @RequestParam
    Map<String, String> parameters) throws HttpRequestMethodNotSupportedException {

        if (!(principal instanceof Authentication)) {
            throw new InsufficientAuthenticationException(
                    "There is no client authentication. Try adding an appropriate authentication filter.");
        }

        String clientId = getClientId(principal);
        ClientDetails authenticatedClient = getClientDetailsService().loadClientByClientId(clientId);

        TokenRequest tokenRequest = getOAuth2RequestFactory().createTokenRequest(parameters, authenticatedClient);

        if (clientId != null && !clientId.equals("")) {
            // Only validate the client details if a client authenticated during this
            // request.
            if (!clientId.equals(tokenRequest.getClientId())) {
                // double check to make sure that the client ID in the token request is the same as that in the
                // authenticated client
                throw new InvalidClientException("Given client ID does not match authenticated client");
            }
        }
        if (authenticatedClient != null) {
            oAuth2RequestValidator.validateScope(tokenRequest, authenticatedClient);
        }
        if (!StringUtils.hasText(tokenRequest.getGrantType())) {
            throw new InvalidRequestException("Missing grant type");
        }
        if (tokenRequest.getGrantType().equals("implicit")) {
            throw new InvalidGrantException("Implicit grant type not supported from token endpoint");
        }

        if (isAuthCodeRequest(parameters)) {
            // The scope was requested or determined during the authorization step
            if (!tokenRequest.getScope().isEmpty()) {
                logger.debug("Clearing scope of incoming token request");
                tokenRequest.setScope(Collections.<String> emptySet());
            }
        }

        if (isRefreshTokenRequest(parameters)) {
            // A refresh token has its own default scopes, so we should ignore any added by the factory here.
            tokenRequest.setScope(OAuth2Utils.parseParameterList(parameters.get(OAuth2Utils.SCOPE)));
        }

        OAuth2AccessToken token = getTokenGranter().grant(tokenRequest.getGrantType(), tokenRequest);
        if (token == null) {
            throw new UnsupportedGrantTypeException("Unsupported grant type: " + tokenRequest.getGrantType());
        }

        return getResponse(token);

    }
}
```

RemoteTokenServices :资源服务可以把传递来的access_token递交给授权服务的/oauth/check_token进行验证，而资源服务自己无需去连接数据库验证access_token，这时就用到了RemoteTokenServices。



### 2.2.1 Oauth的请求封装类

OAuth2Authentication和OAuth2AccessToken是一对好基友，谁要先走谁是狗！！！

#### 2.2.1.1 OAuth2Authentication

**OAuth2Authentication**顾名思义是Authentication的子类，**存储用户信息和客户端信息**，但多了2个属性

```java
private final OAuth2Request storedRequest; 
private final Authentication userAuthentication;
```

这样**OAuth2Authentication**可以存储**2**个Authentication，一个给client(必要)，一个给user(只是有些授权方式需要)。除此之外同样有principle，credentials，authorities，details，authenticated等属性。

**OAuth2Request** 用于存储request中的Authentication信息（grantType,responseType,resouceId,clientId,scope等），这里就引出了OAuth2 中的三大request。



#### 2.2.1.2 OAuth2AccessToken

**OAuth2AccessToken**是一个接口，提供安全令牌token的基本信息，**不包含用户信息，仅包含一些静态属性（scope,tokenType,expires_in等）和getter方法。TokenGranter.grant()**返回的值即**OAuth2AccessToken**。

```java
@org.codehaus.jackson.map.annotate.JsonSerialize(using = OAuth2AccessTokenJackson1Serializer.class)
@org.codehaus.jackson.map.annotate.JsonDeserialize(using = OAuth2AccessTokenJackson1Deserializer.class)
@com.fasterxml.jackson.databind.annotation.JsonSerialize(using = OAuth2AccessTokenJackson2Serializer.class)
@com.fasterxml.jackson.databind.annotation.JsonDeserialize(using = OAuth2AccessTokenJackson2Deserializer.class)

public interface OAuth2AccessToken {

	public static String BEARER_TYPE = "Bearer";

	public static String OAUTH2_TYPE = "OAuth2";

	public static String ACCESS_TOKEN = "access_token";

	public static String TOKEN_TYPE = "token_type";

	public static String EXPIRES_IN = "expires_in";

	public static String REFRESH_TOKEN = "refresh_token";

	public static String SCOPE = "scope";


	Map<String, Object> getAdditionalInformation();

	Set<String> getScope();

	OAuth2RefreshToken getRefreshToken();

	String getTokenType();

	boolean isExpired();

	Date getExpiration();

	int getExpiresIn();

	String getValue();
	
}
```

> **TokenStore同时存储OAuth2AccessToken和OAuth2Authentication**，也可根据OAuth2Authentication中的**OAuth2Request**信息可获取对应的**OAuth2AccessToken**。

**DefaultTokenServices有如下方法，都可以通过一个获得另一个的值** 。

```java
OAuth2AccessToken createAccessToken(OAuth2Authentication authentication)

OAuth2Authentication loadAuthentication(String accessTokenValue)
```

> 当tokenStore是jdbcTokenStore，表示从数据库中根据OAuth2Authentication获取OAuth2AccessToken
> OAuth2AccessToken existingAccessToken = tokenStore.getAccessToken(authentication);



**DefaultOAuth2AccessToken**是OAuth2AccessToken的实现类，多了构造方法，setter方法和OAuth2AccessToken  valueOf(Map<String,Object> tokenParams)。经过json转换后就是我们常见的access_token对象，如下所示。

```json
{
"access_token": "1e95d081-0048-4397-a081-c76f7823fe54",
"token_type": "bearer",
"refresh_token": "7f6db28b-50dc-40a2-b381-3e356e30af2b",
"expires_in": 1799,
"scope": "read write"
}
```



#### 2.2.1.3 BaseRequest及其继承类AuthorizationRequest**、**TokenRequest**、**OAuth2Request

**BaseRequest**是抽象类，有3个属性：clienId、scope和requestParameters。

```java
abstract class BaseRequest implements Serializable {
	private String clientId;
 
	private Set<String> scope = new HashSet<String>();
 
	private Map<String, String> requestParameters = Collections
			.unmodifiableMap(new HashMap<String, String>());
 
       /**  setter,getter  */
}
```

其继承类有**AuthorizationRequest**、**TokenRequest**、**OAuth2Request**。

- **AuthorizationRequest:**向授权服务器AuthorizationEndPoint （**/oauth/authorize**）请求授权，AuthorizationRequest作为载体存储state,redirect_uri等参数，生命周期很短且不能长时间存储信息，可用OAuth2Request代替存储信息。

  ```java
  public class AuthorizationRequest extends BaseRequest implements Serializable {
   
    // 用户同意授权传递的参数，不可改变
    private Map<String, String> approvalParameters = Collections.unmodifiableMap(new HashMap<String, String>());
   
    // 客户端发送出的状态信息，从授权服务器返回的状态应该不变才对
    private String state;
   
    // 返回类型集合
    private Set<String> responseTypes = new HashSet<String>();
   
    // resource ids  可变
    private Set<String> resourceIds = new HashSet<String>();
   
    // 授权的权限
    private Collection<? extends GrantedAuthority> authorities = new HashSet<GrantedAuthority>();
   
    // 终端用户是否同意该request发送
    private boolean approved = false;
   
    // 重定向uri
    private String redirectUri;
   
    // 额外的属性
    private Map<String, Serializable> extensions = new HashMap<String, Serializable>();
   
   
      // 持久化到OAuth2Request
      public OAuth2Request createOAuth2Request() {
        return new OAuth2Request(getRequestParameters(), getClientId(), getAuthorities(), isApproved(), getScope(), getResourceIds(), getRedirectUri(), getResponseTypes(), getExtensions());
    }
   
      // setter,getter
  }
  ```

- **TokenRequest:**向授权服务器TokenEndPoint(**/oauth/token**)发送请求获得access_token时，tokenRequest作为载体存储请求中grantType等参数。常和tokenGranter.grant(grantType,tokenRequest)结合起来使用。
  TokenRequest携带了新属性**grantType**，和方法**createOAuth2Request**（用于持久化）

  ```java
  private String grantType;
  public OAuth2Request createOAuth2Request(ClientDetails client) {
        Map<String, String> requestParameters = getRequestParameters();
        HashMap<String, String> modifiable = new HashMap<String, String>(requestParameters);
        // Remove password if present to prevent leaks
        modifiable.remove("password");
        modifiable.remove("client_secret");
        // Add grant type so it can be retrieved from OAuth2Request
        modifiable.put("grant_type", grantType);
        return new OAuth2Request(modifiable, client.getClientId(), client.getAuthorities(), true, this.getScope(),
  }
  ```

- **OAuth2Request:**用来存储TokenRequest或者AuthorizationRequest的信息，只有构造方法和getter方法，不提供setter方法。它作为**OAuth2Authentication**的一个属性(StoredRequest)，存储request中的authentication信息（authorities,grantType,approved,responseTypes）。

  ```java
  public class OAuth2Request extends BaseRequest implements Serializable {
  
    private static final long serialVersionUID = 1L;
  
    private Set<String> resourceIds = new HashSet<String>();
  
    private Collection<? extends GrantedAuthority> authorities = new HashSet<GrantedAuthority>();
  
    private boolean approved = false;
  
    private TokenRequest refresh = null;
  
    private String redirectUri;
  
    private Set<String> responseTypes = new HashSet<String>();
  
    private Map<String, Serializable> extensions = new HashMap<String, Serializable>();
  
    public OAuth2Request(Map<String, String> requestParameters, String clientId,Collection<? extends GrantedAuthority> authorities, boolean approved, Set<String> scope,Set<String> resourceIds, String redirectUri, Set<String> responseTypes,Map<String, Serializable> extensionProperties) {
        setClientId(clientId);
        setRequestParameters(requestParameters);
        setScope(scope);
        if (resourceIds != null) {
            this.resourceIds = new HashSet<String>(resourceIds);
        }
        if (authorities != null) {
            this.authorities = new HashSet<GrantedAuthority>(authorities);
        }
        this.approved = approved;
        if (responseTypes != null) {
            this.responseTypes = new HashSet<String>(responseTypes);
        }
        this.redirectUri = redirectUri;
        if (extensionProperties != null) {
            this.extensions = extensionProperties;
        }
    }
  
    protected OAuth2Request(OAuth2Request other) {
        this(other.getRequestParameters(), other.getClientId(), other.getAuthorities(), other.isApproved(), other
                .getScope(), other.getResourceIds(), other.getRedirectUri(), other.getResponseTypes(), other
                .getExtensions());
    }
  
    protected OAuth2Request(String clientId) {
        setClientId(clientId);
    }
  
    protected OAuth2Request() {
        super();
    }
  
    public String getRedirectUri() {
        return redirectUri;
    }
  
    public Set<String> getResponseTypes() {
        return responseTypes;
    }
  
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }
  
    public boolean isApproved() {
        return approved;
    }
  
    public Set<String> getResourceIds() {
        return resourceIds;
    }
  
    public Map<String, Serializable> getExtensions() {
        return extensions;
    }
  
    public OAuth2Request createOAuth2Request(Map<String, String> parameters) {
        return new OAuth2Request(parameters, getClientId(), authorities, approved, getScope(), resourceIds,
                redirectUri, responseTypes, extensions);
    }
  
    public OAuth2Request narrowScope(Set<String> scope) {
        OAuth2Request request = new OAuth2Request(getRequestParameters(), getClientId(), authorities, approved, scope,
                resourceIds, redirectUri, responseTypes, extensions);
        request.refresh = this.refresh;
        return request;
    }
  
    public OAuth2Request refresh(TokenRequest tokenRequest) {
        OAuth2Request request = new OAuth2Request(getRequestParameters(), getClientId(), authorities, approved,
                getScope(), resourceIds, redirectUri, responseTypes, extensions);
        request.refresh = tokenRequest;
        return request;
    }
  
    public boolean isRefresh() {
        return refresh != null;
    }
  
    public TokenRequest getRefreshTokenRequest() {
        return refresh;
    }
  
    public String getGrantType() {
        if (getRequestParameters().containsKey(OAuth2Utils.GRANT_TYPE)) {
            return getRequestParameters().get(OAuth2Utils.GRANT_TYPE);
        }
        if (getRequestParameters().containsKey(OAuth2Utils.RESPONSE_TYPE)) {
            String response = getRequestParameters().get(OAuth2Utils.RESPONSE_TYPE);
            if (response.contains("token")) {
                return "implicit";
            }
        }
        return null;
    }
  ```

  

#### 2.2.1.4 OAuth2RefreshToken

**OAuth2RefreshToken**是接口，只有**String getValue()**方法。**DefaultOAuth2RefreshToken**是OAuth2RefreshToken的实现类。

```java
public interface OAuth2RefreshToken {

	/**
	 * The value of the token.
	 * 
	 * @return The value of the token.
	 */
	@JsonValue
	String getValue();

}
```



#### 2.2.1.5 OAuth2RequestFactory接口

工厂类用于生成OAuth2Request、TokenRequest、AuthenticationRequest。

```java
public interface OAuth2RequestFactory {
 
	/**
            * 从request请求参数中获取clientId,scope,state
            * clientDetailsService  loadClientByClientId(clientId) 获取clientDetails resourcesId Authorities
            * 根据以上信息生成AuthenticationRequest
            */
	AuthorizationRequest createAuthorizationRequest(Map<String, String> authorizationParameters);
 
	/**
	 *  AuthorizationRequest request  有生成OAuth2Request的方法
     *  request.createOAuth2Request()
	 */
	OAuth2Request createOAuth2Request(AuthorizationRequest request);
 
 
	OAuth2Request createOAuth2Request(ClientDetails client, TokenRequest tokenRequest);
 
 
	TokenRequest createTokenRequest(Map<String, String> requestParameters, ClientDetails authenticatedClient);
 
 
	TokenRequest createTokenRequest(AuthorizationRequest authorizationRequest, String grantType);
 
}
```



### 2.2.2 TokenGranter、TokenStore、TokenExtractor

#### 2.2.2.1 TokenGranter(/oauth/token)

一般在用户请求TokenEndPoints中的路径/oauth/token时，根据请求参数中的grantType,username,password，client_id,client_secret等，调用TokenGranter给用户分发OAuth2AccessToken。

```java
OAuth2AccessToken token = getTokenGranter().grant(tokenRequest.getGrantType(), tokenRequest);
```

根据grantType(password,authorization-code)和TokenRequest（requestParameters,clientId,grantType）授予人**OAuth2AccessToken**令牌。

```java
public interface TokenGranter {
	OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest);
}
```

> 回忆下TokenRequest包含了基本信息clientId,scope,requestParameters,grantType等。根据tokenRequest获取OAuth2Request，初始化获得OAuth2Authentication，再去数据库里找Oauth2AccessToken，如果有则直接返回，如果没有则创建新的Oauth2AccessToken，并且和OAuth2Authentication一起存入数据库中。



##### AbstractTokenGranter(授予OAuth2AccessToken)

***TokenGranter***抽象继承类**AbstractTokenGranter**，实现了grant方法。

执行顺序为根据**tokenRequest**====》**clientId** ====》**clientDetails**====》**OAuth2Authentication**(getOAuth2Authentication(client,tokenRequest))====》**OAuth2AccessToken**(tokenService.createAccessToken)

通过clientId获取ClientDetails，判断客户端是否有当前正在发起请求的授权模式，调用OAuth2RequestFactory的createOAuth2Request方法传入TokenRequest参数获得OAuth2Request，通过createAccessToken方法将获取的OAuth2Request作为参数获得OAuth2AccessToken。

```java
public abstract class AbstractTokenGranter implements TokenGranter {
	
	protected final Log logger = LogFactory.getLog(getClass());

	private final AuthorizationServerTokenServices tokenServices;

	private final ClientDetailsService clientDetailsService;
	
	private final OAuth2RequestFactory requestFactory;
	
	private final String grantType;

	protected AbstractTokenGranter(AuthorizationServerTokenServices tokenServices,
			ClientDetailsService clientDetailsService, OAuth2RequestFactory requestFactory, String grantType) {
		this.clientDetailsService = clientDetailsService;
		this.grantType = grantType;
		this.tokenServices = tokenServices;
		this.requestFactory = requestFactory;
	}

    //通过grant方法进行认证，获取OAuth2AccessToken
	public OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest) {

		if (!this.grantType.equals(grantType)) {
			return null;
		}
		//通过ClientDetails获取到client进行认证
		String clientId = tokenRequest.getClientId();
		ClientDetails client = clientDetailsService.loadClientByClientId(clientId);
		validateGrantType(grantType, client);

		if (logger.isDebugEnabled()) {
			logger.debug("Getting access token for: " + clientId);
		}

		return getAccessToken(client, tokenRequest);

	}

    //通过OAuth2Authentication获取到OAuth2AccessToken
	protected OAuth2AccessToken getAccessToken(ClientDetails client, TokenRequest tokenRequest) {
		return tokenServices.createAccessToken(getOAuth2Authentication(client, tokenRequest));
	}
	//通过TokenRequest获取到OAuth2Request，通过OAuth2Request获取到OAuth2Authentication
	protected OAuth2Authentication getOAuth2Authentication(ClientDetails client, TokenRequest tokenRequest) {
		OAuth2Request storedOAuth2Request = requestFactory.createOAuth2Request(client, tokenRequest);
		return new OAuth2Authentication(storedOAuth2Request, null);
	}

    //判断客户端是否拥有指定的授权类型，没有则抛出异常
	protected void validateGrantType(String grantType, ClientDetails clientDetails) {
		Collection<String> authorizedGrantTypes = clientDetails.getAuthorizedGrantTypes();
		if (authorizedGrantTypes != null && !authorizedGrantTypes.isEmpty()
				&& !authorizedGrantTypes.contains(grantType)) {
			throw new InvalidClientException("Unauthorized grant type: " + grantType);
		}
	}

	protected AuthorizationServerTokenServices getTokenServices() {
		return tokenServices;
	}
	
	protected OAuth2RequestFactory getRequestFactory() {
		return requestFactory;
	}

}
```

实现AbstractTokenGranter的类有5种。

![21580557-7e210a361f9f6ee8.png](https://upload-images.jianshu.io/upload_images/21580557-162d2b0245bafbb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


其中如果用password的方式进行验证，那么TokenGranter类型是**ResourceOwnerPasswordTokenGranter**，该类中重写了getOAuth2Authentication方法，里面调用了authenticationManager.manage()方法。

`用户可自行定义granter类继承AbstractTokenGranter，重写**getOAuth2Authentication()**方法，并将该granter类添加至CompositeTokenGranter中。`

```java
public class ResourceOwnerPasswordTokenGranter extends AbstractTokenGranter {

	private static final String GRANT_TYPE = "password";

	private final AuthenticationManager authenticationManager;

	public ResourceOwnerPasswordTokenGranter(AuthenticationManager authenticationManager,
			AuthorizationServerTokenServices tokenServices, ClientDetailsService clientDetailsService, OAuth2RequestFactory requestFactory) {
		this(authenticationManager, tokenServices, clientDetailsService, requestFactory, GRANT_TYPE);
	}

	protected ResourceOwnerPasswordTokenGranter(AuthenticationManager authenticationManager, AuthorizationServerTokenServices tokenServices,
			ClientDetailsService clientDetailsService, OAuth2RequestFactory requestFactory, String grantType) {
		super(tokenServices, clientDetailsService, requestFactory, grantType);
		this.authenticationManager = authenticationManager;
	}

    //重写了父类的方法，增加authenticate方法对账号密码进行验证。
	@Override
	protected OAuth2Authentication getOAuth2Authentication(ClientDetails client, TokenRequest tokenRequest) {

		Map<String, String> parameters = new LinkedHashMap<String, String>(tokenRequest.getRequestParameters());
		String username = parameters.get("username");
		String password = parameters.get("password");
		// Protect from downstream leaks of password
		parameters.remove("password");

		Authentication userAuth = new UsernamePasswordAuthenticationToken(username, password);
		((AbstractAuthenticationToken) userAuth).setDetails(parameters);
		try {
			userAuth = authenticationManager.authenticate(userAuth);
		}
		catch (AccountStatusException ase) {
			//covers expired, locked, disabled cases (mentioned in section 5.2, draft 31)
			throw new InvalidGrantException(ase.getMessage());
		}
		catch (BadCredentialsException e) {
			// If the username/password are wrong the spec says we should send 400/invalid grant
			throw new InvalidGrantException(e.getMessage());
		}
		if (userAuth == null || !userAuth.isAuthenticated()) {
			throw new InvalidGrantException("Could not authenticate user: " + username);
		}
		
		OAuth2Request storedOAuth2Request = getRequestFactory().createOAuth2Request(client, tokenRequest);		
		return new OAuth2Authentication(storedOAuth2Request, userAuth);
	}
}
```



##### CompositeTokenGranter

TokenGranter有继承类**CompositeTokenGranter**，包含List<TokenGranter> tokenGranters属性，grant方法是遍历tokenGranters进行逐一grant，只要有一个有返回值就返回。

```java
public class CompositeTokenGranter implements TokenGranter {

	private final List<TokenGranter> tokenGranters;

	public CompositeTokenGranter(List<TokenGranter> tokenGranters) {
		this.tokenGranters = new ArrayList<TokenGranter>(tokenGranters);
	}
	
    //对所有tokenGranters继承类进行遍历
	public OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest) {
		for (TokenGranter granter : tokenGranters) {
			OAuth2AccessToken grant = granter.grant(grantType, tokenRequest);
			if (grant!=null) {
				return grant;
			}
		}
		return null;
	}
	
	public void addTokenGranter(TokenGranter tokenGranter) {
		if (tokenGranter == null) {
			throw new IllegalArgumentException("Token granter is null");
		}
		tokenGranters.add(tokenGranter);
	}

}
```



#### 2.2.2.2 TokenStore

一般在TokenGranter执行grant方法完毕后，TokenStore将OAuth2AccessToken和OAuth2Authentication存储起来，方便以后根据其中一个查询另外一个（如根据access_token查询获得OAuth2Authentication）。

存储**OAuth2AccessToken**和**OAuth2Authentication**（比Authentication多了两个属性storedRequest，userAuthentication），存储方法如下。还有各种read，remove方法。

```java
public interface TokenStore {

	void storeAccessToken(OAuth2AccessToken token, OAuth2Authentication authentication);

	OAuth2Authentication readAuthentication(OAuth2AccessToken token);
	
	OAuth2Authentication readAuthentication(String token);

	OAuth2AccessToken readAccessToken(String tokenValue);

	void removeAccessToken(OAuth2AccessToken token);

	void storeRefreshToken(OAuth2RefreshToken refreshToken, OAuth2Authentication authentication);

	OAuth2RefreshToken readRefreshToken(String tokenValue);

	OAuth2Authentication readAuthenticationForRefreshToken(OAuth2RefreshToken token);

	void removeRefreshToken(OAuth2RefreshToken token);

	void removeAccessTokenUsingRefreshToken(OAuth2RefreshToken refreshToken);

	OAuth2AccessToken getAccessToken(OAuth2Authentication authentication);

	Collection<OAuth2AccessToken> findTokensByClientIdAndUserName(String clientId, String userName);

	Collection<OAuth2AccessToken> findTokensByClientId(String clientId);

}
```

**TokenStore**的实现类有5类，其中**JdbcTokenStore**是通过连接数据库来存储OAuth2AccessToken的，这也是我们一般存储token的方法。条件是数据库里的表结构必须按照标准建立。

![21580557-4ce2c9dbee0ea3bb.png](https://upload-images.jianshu.io/upload_images/21580557-309e0cbbbc93a7c2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**JdbcTokenStore：**oauth_access_token表结构如下，可见表里存储了OAuth2AccessToken和OAuth2Authentication两个对象，值得注意的是token_id并不等于OAuth2AccessToken.getValue()，value经过MD5加密后才是token_id。同理authentication_id 和 refresh_token也是经过加密转换存储的。第一次获得token，直接存入数据库表里。如果重复post请求/oauth/token，  JdbcTokenStore会先判断表中是否已有该用户的token，如果有先删除，再添加。

![21580557-20289ba5cc4ca997.png](https://upload-images.jianshu.io/upload_images/21580557-b565f7dd621246f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**JwtTokenStore：**不存储token和authentication,直接根据token解析获得authentication。



#### 2.2.2.3 TokenExtractor (OAuth2AuthenticationProcessingFilter)

用户携带token访问资源，过滤器进行到**OAuth2AuthenticationProcessingFilter**时，从HttpServletRequest中获取Authorization或access_token(可以从header或者params中获取)，拼接成PreAuthenticatedAuthenticationToken**(Authentication子类)**

**BearerTokenExtractor**是它的实现类，实现了从request中获取Authentication的方法。

1. header中  Authentication:Bearer xxxxxxxx--xxx
2. request parameters中  access_token=xxxx-xxxx-xxxx

如果都不存在，则不是Oauth2的认证方式。

```java
public class BearerTokenExtractor implements TokenExtractor {

	private final static Log logger = LogFactory.getLog(BearerTokenExtractor.class);

    //从HttpServletRequest中获取access_token
	@Override
	public Authentication extract(HttpServletRequest request) {
		String tokenValue = extractToken(request);
		if (tokenValue != null) {
			PreAuthenticatedAuthenticationToken authentication = new PreAuthenticatedAuthenticationToken(tokenValue, "");
			return authentication;
		}
		return null;
	}

    //从请求参数中获取access_token=xxxx-xxxx-xxxx，并在请求头中添加token类型；
	protected String extractToken(HttpServletRequest request) {
		// first check the header...
		String token = extractHeaderToken(request);

		// bearer type allows a request parameter as well
		if (token == null) {
			logger.debug("Token not found in headers. Trying request parameters.");
			token = request.getParameter(OAuth2AccessToken.ACCESS_TOKEN);
			if (token == null) {
				logger.debug("Token not found in request parameters.  Not an OAuth2 request.");
			}
			else {
				request.setAttribute(OAuth2AuthenticationDetails.ACCESS_TOKEN_TYPE, OAuth2AccessToken.BEARER_TYPE);
			}
		}

		return token;
	}

	//从请求头中获取Authentication:Bearer xxxxxxxx--xxx，并在请求头中添加token类型。
	protected String extractHeaderToken(HttpServletRequest request) {
		Enumeration<String> headers = request.getHeaders("Authorization");
		while (headers.hasMoreElements()) { // typically there is only one (most servers enforce that)
			String value = headers.nextElement();
			if ((value.toLowerCase().startsWith(OAuth2AccessToken.BEARER_TYPE.toLowerCase()))) {
				String authHeaderValue = value.substring(OAuth2AccessToken.BEARER_TYPE.length()).trim();
				// Add this here for the auth details later. Would be better to change the signature of this method.
				request.setAttribute(OAuth2AuthenticationDetails.ACCESS_TOKEN_TYPE,
						value.substring(0, OAuth2AccessToken.BEARER_TYPE.length()).trim());
				int commaIndex = authHeaderValue.indexOf(',');
				if (commaIndex > 0) {
					authHeaderValue = authHeaderValue.substring(0, commaIndex);
				}
				return authHeaderValue;
			}
		}

		return null;
	}

}
```



#### 2.2.2.4 ResourceServerTokenServices

两个方法。用户携access_token访问资源服务器时，资源服务器会将该字符串进行解析，获得OAuth2Authentication和OAuth2AccessToken。

loadAuthentication根据字符串accessToken获得OAuth2Authentication;

readAccessToken根据字符串accessToken获得OAuth2AccessToken。

```java
public interface ResourceServerTokenServices {
	//根据字符串accessToken获得OAuth2Authentication
	OAuth2Authentication loadAuthentication(String accessToken) throws AuthenticationException, InvalidTokenException;
	//根据字符串accessToken获得OAuth2AccessToken
	OAuth2AccessToken readAccessToken(String accessToken);

}
```



##### DefaultTokenServices

实现了两个接口AuthorizationServerTokenServices和ResourceServerTokenServices。常在granter().grant()方法中调用tokenServices.createAccessToken()方法获得oauth2accesstoken。

**OAuth2AccessToken**

```java
public interface AuthorizationServerTokenServices {

	OAuth2AccessToken createAccessToken(OAuth2Authentication authentication) throws AuthenticationException;

	OAuth2AccessToken refreshAccessToken(String refreshToken, TokenRequest tokenRequest)
			throws AuthenticationException;

	OAuth2AccessToken getAccessToken(OAuth2Authentication authentication);
    
}
```

![21580557-e10ad7024f80873a.png](https://upload-images.jianshu.io/upload_images/21580557-e50d5cd8b8d47181.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


其中重要方法createAccessToken(OAuth2Authentication oauth2)源码如下

```java
	@Transactional
	public OAuth2AccessToken createAccessToken(OAuth2Authentication authentication) throws AuthenticationException {

		OAuth2AccessToken existingAccessToken = tokenStore.getAccessToken(authentication);
		OAuth2RefreshToken refreshToken = null;
		if (existingAccessToken != null) {
			if (existingAccessToken.isExpired()) {
				if (existingAccessToken.getRefreshToken() != null) {
					refreshToken = existingAccessToken.getRefreshToken();
					// The token store could remove the refresh token when the
					// access token is removed, but we want to
					// be sure...
					tokenStore.removeRefreshToken(refreshToken);
				}
				tokenStore.removeAccessToken(existingAccessToken);
			}
			else {
				// Re-store the access token in case the authentication has changed
				tokenStore.storeAccessToken(existingAccessToken, authentication);
				return existingAccessToken;
			}
		}

		// 在access_token没有关联的refresh_token的情况下才能创建refresh_token，如果有的话会重复利用
		if (refreshToken == null) {
			refreshToken = createRefreshToken(authentication);
		}
		// 如果refresh_token过期了需要重新发布
		else if (refreshToken instanceof ExpiringOAuth2RefreshToken) {
			ExpiringOAuth2RefreshToken expiring = (ExpiringOAuth2RefreshToken) refreshToken;
			if (System.currentTimeMillis() > expiring.getExpiration().getTime()) {
				refreshToken = createRefreshToken(authentication);
			}
		}
		
		OAuth2AccessToken accessToken = createAccessToken(authentication, refreshToken);
		tokenStore.storeAccessToken(accessToken, authentication);
		// In case it was modified
		refreshToken = accessToken.getRefreshToken();
		if (refreshToken != null) {
			tokenStore.storeRefreshToken(refreshToken, authentication);
		}
		return accessToken;

	}
```



##### RemoteTokenServices

当授权服务和资源服务不在一个应用程序的时候，资源服务可以把传递来的access_token递交给授权服务的**/oauth/check_token**进行验证，而资源服务自己无需去连接数据库验证access_token，这时就用到了RemoteTokenServices。

loadAuthentication方法，设置head表头Authorization 存储clientId和clientSecret信息，请求参数包含access_token字符串，向AuthServer的**CheckTokenEndpoint** (/oauth/check_token)发送请求，返回验证结果map（包含clientId,grantType,scope,username等信息），拼接成OAuth2Authentication。



`AuthServer需要配置checkTokenAccess，否则默认为“denyAll()”，请求访问/oauth/check_token会提示没权限。`

```java
        @Override
        public void configure(AuthorizationServerSecurityConfigurer oauthServer) {
            oauthServer.realm(QQ_RESOURCE_ID).allowFormAuthenticationForClients();
 
            // 访问/oauth/check_token 需要client验证
            oauthServer.checkTokenAccess("isAuthenticated()");、
            // 也可配置访问/oauth/check_token无需验证
            // oauthServer.checkTokenAccess("permitAll()");
        }
```

不支持readAccessToken方法。

```java
public class RemoteTokenServices implements ResourceServerTokenServices {

	protected final Log logger = LogFactory.getLog(getClass());

	private RestOperations restTemplate;

	private String checkTokenEndpointUrl;

	private String clientId;

	private String clientSecret;

    private String tokenName = "token";

	private AccessTokenConverter tokenConverter = new DefaultAccessTokenConverter();

	public RemoteTokenServices() {
		restTemplate = new RestTemplate();
		((RestTemplate) restTemplate).setErrorHandler(new DefaultResponseErrorHandler() {
			@Override
			// Ignore 400
			public void handleError(ClientHttpResponse response) throws IOException {
				if (response.getRawStatusCode() != 400) {
					super.handleError(response);
				}
			}
		});
	}

	public void setRestTemplate(RestOperations restTemplate) {
		this.restTemplate = restTemplate;
	}

	public void setCheckTokenEndpointUrl(String checkTokenEndpointUrl) {
		this.checkTokenEndpointUrl = checkTokenEndpointUrl;
	}

	public void setClientId(String clientId) {
		this.clientId = clientId;
	}

	public void setClientSecret(String clientSecret) {
		this.clientSecret = clientSecret;
	}

	public void setAccessTokenConverter(AccessTokenConverter accessTokenConverter) {
		this.tokenConverter = accessTokenConverter;
	}

    public void setTokenName(String tokenName) {
        this.tokenName = tokenName;
    }

    @Override
	public OAuth2Authentication loadAuthentication(String accessToken) throws AuthenticationException, InvalidTokenException {

		MultiValueMap<String, String> formData = new LinkedMultiValueMap<String, String>();
		formData.add(tokenName, accessToken);
		HttpHeaders headers = new HttpHeaders();
		headers.set("Authorization", getAuthorizationHeader(clientId, clientSecret));
		Map<String, Object> map = postForMap(checkTokenEndpointUrl, formData, headers);

		if (map.containsKey("error")) {
			if (logger.isDebugEnabled()) {
				logger.debug("check_token returned error: " + map.get("error"));
			}
			throw new InvalidTokenException(accessToken);
		}

		// gh-838
		if (!Boolean.TRUE.equals(map.get("active"))) {
			logger.debug("check_token returned active attribute: " + map.get("active"));
			throw new InvalidTokenException(accessToken);
		}

		return tokenConverter.extractAuthentication(map);
	}

	@Override
	public OAuth2AccessToken readAccessToken(String accessToken) {
		throw new UnsupportedOperationException("Not supported: read access token");
	}

	private String getAuthorizationHeader(String clientId, String clientSecret) {

		if(clientId == null || clientSecret == null) {
			logger.warn("Null Client ID or Client Secret detected. Endpoint that requires authentication will reject request with 401 error.");
		}

		String creds = String.format("%s:%s", clientId, clientSecret);
		try {
			return "Basic " + new String(Base64.encode(creds.getBytes("UTF-8")));
		}
		catch (UnsupportedEncodingException e) {
			throw new IllegalStateException("Could not convert String");
		}
	}

	private Map<String, Object> postForMap(String path, MultiValueMap<String, String> formData, HttpHeaders headers) {
		if (headers.getContentType() == null) {
			headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
		}
		@SuppressWarnings("rawtypes")
		Map map = restTemplate.exchange(path, HttpMethod.POST,
				new HttpEntity<MultiValueMap<String, String>>(formData, headers), Map.class).getBody();
		@SuppressWarnings("unchecked")
		Map<String, Object> result = map;
		return result;
	}

}
```



### 2.2.3 Client客户端相关类  ClientDetails   ClientDetailsService

就是UserDetails和UserDetailsService的翻版。一个是对应user，一个是对应client。

client需要**事先注册**到授权服务器，这样授权服务器会根据client的授权请求获取clientId，secret等信息，进行验证后返回token。

#### 2.2.3.1 ClientDetails

client的信息，**存于授权服务器端**，这样只需要知道客户端的clientId，就可以获取到客户端能访问哪些资源，是否需要密码，是否限制了scope，拥有的权限等等。

```java
public interface ClientDetails extends Serializable {
 
	String getClientId();
 
	// client能访问的资源id
	Set<String> getResourceIds();
 
	// 验证client是否需要密码
	boolean isSecretRequired();
 
	
	String getClientSecret();
 
	// client是否限制了scope
	boolean isScoped();
 
	// scope集合
	Set<String> getScope();
 
	// 根据哪些grantType验证通过client
	Set<String> getAuthorizedGrantTypes();
 
	// 注册成功后跳转的uri
	Set<String> getRegisteredRedirectUri();
 
	// client拥有的权限
	Collection<GrantedAuthority> getAuthorities();
 
	// client的token时效
	Integer getAccessTokenValiditySeconds();
 
	// client的refreshToken时效
	Integer getRefreshTokenValiditySeconds();
	
	// true:默认自动授权；false:需要用户确定才能授权
	boolean isAutoApprove(String scope);
 
	// 额外的信息
	Map<String, Object> getAdditionalInformation();
 
}
```



#### 2.2.3.2 ClientDetailsService

只有一个loadClientByClientId方法，根据clientId获取clientDetails对象。

```java
public interface ClientDetailsService {

  /**
   * Load a client by the client id. This method must not return null.
   *
   * @param clientId The client id.
   * @return The client details (never null).
   * @throws ClientRegistrationException If the client account is locked, expired, disabled, or invalid for any other reason.
   */
  ClientDetails loadClientByClientId(String clientId) throws ClientRegistrationException;

}
```

**有两个子类**

- **InMemoryClientDetailsService（内存）**：把ClientDetails存内存
- **JdbcClientDetailsService**：存数据库里（oauth_client_details表）



在AuthorizationServerConfigurerAdapter类中的configure方法中配置客户端信息存储方式：

```java
//存储在数据库中：
	@Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.withClientDetails(clientDetails());
    }
    
//或存储在内存中：
	@Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
 
        // @formatter:off
        clients.inMemory().withClient("aiqiyi")
              .resourceIds(QQ_RESOURCE_ID)
              .authorizedGrantTypes("authorization_code", "refresh_token", "implicit")
              .authorities("ROLE_CLIENT")
              // , "get_fanslist"
              .scopes("get_fanslist")
              .secret("secret")
              .redirectUris("http://localhost:8081/aiqiyi/qq/redirect")
              .autoApprove(true)
              .autoApprove("get_user_info")
              .and()
              .withClient("youku")
              .resourceIds(QQ_RESOURCE_ID)
              .authorizedGrantTypes("authorization_code", "refresh_token", "implicit")
              .authorities("ROLE_CLIENT")
              .scopes("get_user_info", "get_fanslist")
              .secret("secret")
              .redirectUris("http://localhost:8082/youku/qq/redirect");
    }
```



#### 2.2.3.3 ClientDetailsServiceBuilder

创建**InMemoryClientDetailsService**或者**JdbcClientDetailsService**，有内部类ClientDetailsServiceBuilder。

```java
public class ClientDetailsServiceBuilder<B extends ClientDetailsServiceBuilder<B>> extends
		SecurityConfigurerAdapter<ClientDetailsService, B> implements SecurityBuilder<ClientDetailsService> {
 
	private List<ClientBuilder> clientBuilders = new ArrayList<ClientBuilder>();
 
	public InMemoryClientDetailsServiceBuilder inMemory() throws Exception {
		return new InMemoryClientDetailsServiceBuilder();
	}
 
	public JdbcClientDetailsServiceBuilder jdbc() throws Exception {
		return new JdbcClientDetailsServiceBuilder();
	}
 
	@SuppressWarnings("rawtypes")
	public ClientDetailsServiceBuilder<?> clients(final ClientDetailsService clientDetailsService) throws Exception {
		return new ClientDetailsServiceBuilder() {
			@Override
			public ClientDetailsService build() throws Exception {
				return clientDetailsService;
			}
		};
	}
 
    // clients.inMemory().withClient("clientId").scopes().secret()...
	public ClientBuilder withClient(String clientId) {
		ClientBuilder clientBuilder = new ClientBuilder(clientId);
		this.clientBuilders.add(clientBuilder);
		return clientBuilder;
	}
 
	@Override
	public ClientDetailsService build() throws Exception {
		for (ClientBuilder clientDetailsBldr : clientBuilders) {
			addClient(clientDetailsBldr.clientId, clientDetailsBldr.build());
		}
		return performBuild();
	}
 
	protected void addClient(String clientId, ClientDetails build) {
	}
 
	protected ClientDetailsService performBuild() {
		throw new UnsupportedOperationException("Cannot build client services (maybe use inMemory() or jdbc()).");
	}
 
	public final class ClientBuilder {
         // ...
         public ClientDetailsServiceBuilder<B> and() {
			return ClientDetailsServiceBuilder.this;
		}
    }
}
```



#### 2.2.4 资源服务器配置  ResourceServerConfigurerAdapter

配置哪些路径需要认证后才能访问，哪些不需要。自然就联想到了**HttpSecurity**（配置HttpSecurity就相当于配置了不同uri对应的filters）。

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter
{
 
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .csrf().disable()
                .authorizeRequests()
                .anyRequest().authenticated()//所有请求必须登陆后访问
                .and().httpBasic()
                .and()
                    .formLogin()
                    .loginPage("/login")
                    .defaultSuccessUrl("/index")
                    .failureUrl("/login?error")
                    .permitAll()//登录界面，错误界面可以直接访问
                .and()
                .logout().logoutUrl("/logout").logoutSuccessUrl("/login")
                .permitAll().and().rememberMe();//注销请求可直接访问
    }
 
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication().withUser("user").password("password").roles("USER").and()
                .withUser("admin").password("password").roles("USER", "ADMIN");
    }
}
```

作为资源服务器**ResourceServerConfigurerAdapter**，需要和@EnableResourceServer搭配，然后和上面一样需配置HttpSecurity就好了。还能配置ResourceServerSecurityConfigurer，设置tokenService等。

```java
/**
 * 配置资源服务器
*/
@Configuration
@EnableResourceServer
protected static class ResourceServerConfiguration extends ResourceServerConfigurerAdapter {
 
    @Autowired
    private CustomAuthenticationEntryPoint customAuthenticationEntryPoint;

    @Autowired
    private CustomLogoutSuccessHandler customLogoutSuccessHandler;

    @Override
    public void configure(HttpSecurity http) throws Exception {

    	http
            .exceptionHandling()
            .authenticationEntryPoint(customAuthenticationEntryPoint)
            .and()
            .logout()
            .logoutUrl("/oauth/logout")
            .logoutSuccessHandler(customLogoutSuccessHandler)
            .and()
            .authorizeRequests()
            // hello路径允许直接访问
            .antMatchers("/hello/").permitAll()
            // secure路径需要验证后才能访问
            .antMatchers("/secure/**").authenticated();
    }
 
 
    // 远程连接authServer服务
    @Autowired
    public RemoteTokenServices remoteTokenServices;
	
	@Override
	public void configure(ResourceServerSecurityConfigurer resources) throws Exception {
		resources.tokenServices(remoteTokenServices);
	}
}
```



### 2.2.5 授权服务器配置    AuthorizationServerConfigurerAdapter

注册client信息，可以同时配置多个不同类型的client。

```java
@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {

    @Resource
    private BCryptPasswordEncoder bCryptPasswordEncoder;

    //token存储方式
    @Resource
    private TokenStore tokenStore;
    //JWT令牌配置
    @Resource
    private JwtAccessTokenConverter accessTokenConverter;

    //客户端详情服务
    @Autowired
    private ClientDetailsService clientDetailsService;

    //认证管理器
    @Autowired
    private AuthenticationManager authenticationManager;


    /**
     * 将客户端信息存储到数据库
     *
     * @param dataSource
     * @return
     */
    @Bean
    public ClientDetailsService clientDetailsService(DataSource dataSource) {
        ClientDetailsService clientDetailsService = new JdbcClientDetailsService(dataSource);
        ((JdbcClientDetailsService)clientDetailsService).setPasswordEncoder(bCryptPasswordEncoder);
        return clientDetailsService;
    }

    /**
     * 客户端配置
     *
     * @param clients
     * @throws Exception
     */
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.withClientDetails(clientDetailsService);
//        clients.inMemory()//使用内存存储
//                .withClient("c1") //客户端id
//                .secret(bCryptPasswordEncoder.encode("abc123"))//设置密码
//                .resourceIds("res1")//可访问的资源列表
//                .authorizedGrantTypes("authorization_code", "password", "client_credentials", "implicit", "refresh_token")//该client允许的授权类型
//                .scopes("all")//允许的授权范围
//                .autoApprove(false)//false跳转到授权页面，true不跳转
//                .redirectUris("http://www.baidu.com");//设置回调地址
    }


    /**
     * 令牌管理服务
     *
     * @return
     */
    @Bean
    public AuthorizationServerTokenServices tokenServices() {
        DefaultTokenServices services = new DefaultTokenServices();
        services.setClientDetailsService(clientDetailsService); //客户端详情服务
        services.setSupportRefreshToken(true); //支持刷新令牌
        services.setTokenStore(tokenStore); //令牌的存储策略
        //令牌增强,设置JWT令牌
        TokenEnhancerChain tokenEnhancerChain = new TokenEnhancerChain();
        tokenEnhancerChain.setTokenEnhancers(Arrays.asList(accessTokenConverter));
        services.setTokenEnhancer(tokenEnhancerChain);

        services.setAccessTokenValiditySeconds(7200); //令牌默认有效时间2小时
        services.setRefreshTokenValiditySeconds(259200); //刷新令牌默认有效期3天
        return services;
    }

    /**
     * 设置授权码模式的授权码如何存取，暂时采用内存方式
     *
     * @return
     */
//    @Bean
//    public AuthorizationCodeServices authorizationCodeServices(){
//        return new InMemoryAuthorizationCodeServices();
//    }

    @Resource
    private AuthorizationCodeServices authorizationCodeServices;

    /**
     * 授权码存储到数据库
     * @param dataSource
     * @return
     */
    @Bean
    public AuthorizationCodeServices authorizationCodeServices(DataSource dataSource){
        return new JdbcAuthorizationCodeServices(dataSource);
    }

    /**
     * 令牌访问端点配置
     *
     * @param endpoints
     * @throws Exception
     */
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints
                .authenticationManager(authenticationManager)//认证管理器
                .authorizationCodeServices(authorizationCodeServices)//授权码服务
                .tokenServices(tokenServices()) //令牌管理服务（设置令牌存储方式和令牌类型JWT）
                .allowedTokenEndpointRequestMethods(HttpMethod.POST);
    }

    /**
     * 对授权端点接口的安全约束
     *
     * @param security
     * @throws Exception
     */
    @Override
    public void configure(AuthorizationServerSecurityConfigurer security) throws Exception {
        security
                .tokenKeyAccess("permitAll()") // /auth/token_key是公开的
                .checkTokenAccess("permitAll()") // /auth/check_token是公开的
                .allowFormAuthenticationForClients(); //允许表单认证（申请令牌）
    }

}
```



### 2.2.6 TokenEndPoint，AuthorizationEndPoint，CheckTokenEndPoint

#### 2.2.6.1 TokenEndPoint

客户端post请求"/oauth/token"，验证用户信息并获取OAuth2AccessToken，必须先经过client验证。这一步的最终目的是存储OAuth2AccessToken+OAuth2Authentication并返回OAuth2AccessToken。

```java
	@RequestMapping(value = "/oauth/token", method=RequestMethod.POST)
	public ResponseEntity<OAuth2AccessToken>	 postAccessToken(Principal principal, 	@RequestParam Map<String, String> parameters) throws HttpRequestMethodNotSupportedException {
 
		if (!(principal instanceof Authentication)) {
			throw new InsufficientAuthenticationException(
					"There is no client authentication. Try adding an appropriate authentication filter.");
		}
 
		String clientId = getClientId(principal);
		ClientDetails authenticatedClient = getClientDetailsService().loadClientByClientId(clientId);
 
		TokenRequest tokenRequest = getOAuth2RequestFactory().createTokenRequest(parameters, authenticatedClient);
 
		...
        // AuthorizationServerEndpointsConfigurer
		OAuth2AccessToken token = getTokenGranter().grant(tokenRequest.getGrantType(), tokenRequest);
		if (token == null) {
			throw new UnsupportedGrantTypeException("Unsupported grant type: " + tokenRequest.getGrantType());
		}
 
		return getResponse(token);
	}
```



#### 2.2.6.2 AuthorizationEndPoint

这个一般只适用于authorization code模式，客户端请求authorization server中的/oauth/authorize（请求前先得登录oauth server获得authentication），验证client信息后根据redirect_uri请求重定向回client，同时带上code值。client附带code值再次向/oauth/token请求，返回accesstoken。

```java
    @RequestMapping(value = "/oauth/authorize")
	public ModelAndView authorize(Map<String, Object> model, @RequestParam Map<String, String> parameters,
			SessionStatus sessionStatus, Principal principal) {
 
		// Pull out the authorization request first, using the OAuth2RequestFactory. All further logic should
		// query off of the authorization request instead of referring back to the parameters map. The contents of the
		// parameters map will be stored without change in the AuthorizationRequest object once it is created.
		AuthorizationRequest authorizationRequest = getOAuth2RequestFactory().createAuthorizationRequest(parameters);
 
		Set<String> responseTypes = authorizationRequest.getResponseTypes();
 
		if (!responseTypes.contains("token") && !responseTypes.contains("code")) {
			throw new UnsupportedResponseTypeException("Unsupported response types: " + responseTypes);
		}
 
		if (authorizationRequest.getClientId() == null) {
			throw new InvalidClientException("A client id must be provided");
		}
 
		try {
 
			if (!(principal instanceof Authentication) || !((Authentication) principal).isAuthenticated()) {
				throw new InsufficientAuthenticationException(
						"User must be authenticated with Spring Security before authorization can be completed.");
			}
 
			ClientDetails client = getClientDetailsService().loadClientByClientId(authorizationRequest.getClientId());
 
			// The resolved redirect URI is either the redirect_uri from the parameters or the one from
			// clientDetails. Either way we need to store it on the AuthorizationRequest.
			String redirectUriParameter = authorizationRequest.getRequestParameters().get(OAuth2Utils.REDIRECT_URI);
			String resolvedRedirect = redirectResolver.resolveRedirect(redirectUriParameter, client);
			if (!StringUtils.hasText(resolvedRedirect)) {
				throw new RedirectMismatchException(
						"A redirectUri must be either supplied or preconfigured in the ClientDetails");
			}
			authorizationRequest.setRedirectUri(resolvedRedirect);
 
			// We intentionally only validate the parameters requested by the client (ignoring any data that may have
			// been added to the request by the manager).
			oauth2RequestValidator.validateScope(authorizationRequest, client);
 
			// Some systems may allow for approval decisions to be remembered or approved by default. Check for
			// such logic here, and set the approved flag on the authorization request accordingly.
			authorizationRequest = userApprovalHandler.checkForPreApproval(authorizationRequest,
					(Authentication) principal);
			// TODO: is this call necessary?
			boolean approved = userApprovalHandler.isApproved(authorizationRequest, (Authentication) principal);
			authorizationRequest.setApproved(approved);
 
			// Validation is all done, so we can check for auto approval...
			if (authorizationRequest.isApproved()) {
				if (responseTypes.contains("token")) {
					return getImplicitGrantResponse(authorizationRequest);
				}
				if (responseTypes.contains("code")) {
                                 // 生成code值并返回
					return new ModelAndView(getAuthorizationCodeResponse(authorizationRequest,
							(Authentication) principal));
				}
			}
 
			// Place auth request into the model so that it is stored in the session
			// for approveOrDeny to use. That way we make sure that auth request comes from the session,
			// so any auth request parameters passed to approveOrDeny will be ignored and retrieved from the session.
			model.put("authorizationRequest", authorizationRequest);
 
			return getUserApprovalPageResponse(model, authorizationRequest, (Authentication) principal);
 
		}
		catch (RuntimeException e) {
			sessionStatus.setComplete();
			throw e;
		}
 
	}
```



#### 2.2.6.3 CheckTokenEndpoint

当采用RemoteTokenServices时，resouceServer无法自行验证access_token字符串是否正确，遂递交给另一个应用程序中的authserver里CheckTokenEndpoint(/oauth/check_token)进行检验，检验结果返回给resourceServer。

```java
	@RequestMapping(value = "/oauth/check_token")
	@ResponseBody
	public Map<String, ?> checkToken(@RequestParam("token") String value) {
 
		OAuth2AccessToken token = resourceServerTokenServices.readAccessToken(value);
		if (token == null) {
			throw new InvalidTokenException("Token was not recognised");
		}
 
		if (token.isExpired()) {
			throw new InvalidTokenException("Token has expired");
		}
 
		OAuth2Authentication authentication = resourceServerTokenServices.loadAuthentication(token.getValue());
 
		Map<String, ?> response = accessTokenConverter.convertAccessToken(token, authentication);
 
		return response;
	}
```







# 三、异常处理源码

## 3.1 概述

**异常处理规则：**

- 规则1. 如果异常是 AuthenticationException，使用 AuthenticationEntryPoint 处理
- 规则2. 如果异常是 AccessDeniedException 且用户是匿名用户，使用 AuthenticationEntryPoint 处理
- 规则3. 如果异常是 AccessDeniedException 且用户不是匿名用户，如果否则交给 AccessDeniedHandler 处理。



## 3.2 源码

### 3.2.1 ExceptionTranslationFilter

#### ExceptionTranslationFilter的doFilter

ExceptionTranslationFilter是个异常过滤器，用来处理在认证授权过程中抛出的异常，在过滤器链中处于倒数第三的位置（这个filter后面分为是FilterSecurityInterceptor、SwitchUserFilter），所以ExceptionTranslationFilter只能捕获到后面两个过滤器所抛出的异常。 



ExceptionTranslationFilter后面的过滤器是FilterSecurityInterceptor。先上一张图，如下图1所示：

![21580557-0fd084a033d2b022.png](https://upload-images.jianshu.io/upload_images/21580557-71df897989670cef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




- 红框1中的，是调用Filter链中的后续Filter。
- 如果图1中的操作抛出异常，就会来到红框2处，判断抛出的异常是否是AuthenticationException。
- 如果抛出的异常不是AuthenticationException，即红框2的结果为null，那么就到红框3处，判断是否是AccessDeniedException。
- 如果抛出的异常是AuthenticationException或者时AccessDeniedException，那么执行红框4处的代码。



#### ExceptionTranslationFilter的handleSpringSecurityException方法

下面来看handleSpringSecurityException的方法体

```java
public class ExceptionTranslationFilter extends GenericFilterBean {

    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        try {
            chain.doFilter(request, response);

            logger.debug("Chain processed normally");
        }
        catch (IOException ex) {
            throw ex;
        }
        catch (Exception ex) {
            // Try to extract a SpringSecurityException from the stacktrace
            Throwable[] causeChain = throwableAnalyzer.determineCauseChain(ex);
            RuntimeException ase = (AuthenticationException) throwableAnalyzer
                    .getFirstThrowableOfType(AuthenticationException.class, causeChain);

            if (ase == null) {
                ase = (AccessDeniedException) throwableAnalyzer.getFirstThrowableOfType(
                        AccessDeniedException.class, causeChain);
            }

            if (ase != null) {
                if (response.isCommitted()) {
                    throw new ServletException("Unable to handle the Spring Security Exception because the response is already committed.", ex);
                }
                handleSpringSecurityException(request, response, chain, ase);
            }
            else {
                // Rethrow ServletExceptions and RuntimeExceptions as-is
                if (ex instanceof ServletException) {
                    throw (ServletException) ex;
                }
                else if (ex instanceof RuntimeException) {
                    throw (RuntimeException) ex;
                }

                // Wrap other Exceptions. This shouldn't actually happen
                // as we've already covered all the possibilities for doFilter
                throw new RuntimeException(ex);
            }
        }
    }

    private void handleSpringSecurityException(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain, RuntimeException exception)
            throws IOException, ServletException {
        if (exception instanceof AuthenticationException) {
            logger.debug(
                    "Authentication exception occurred; redirecting to authentication entry point",
                    exception);

            sendStartAuthentication(request, response, chain,
                    (AuthenticationException) exception);
        }
        else if (exception instanceof AccessDeniedException) {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authenticationTrustResolver.isAnonymous(authentication) || authenticationTrustResolver.isRememberMe(authentication)) {
                logger.debug(
                        "Access is denied (user is " + (authenticationTrustResolver.isAnonymous(authentication) ? "anonymous" : "not fully authenticated") + "); redirecting to authentication entry point",
                        exception);

                sendStartAuthentication(
                        request,
                        response,
                        chain,
                        new InsufficientAuthenticationException(
                            messages.getMessage(
                                "ExceptionTranslationFilter.insufficientAuthentication",
                                "Full authentication is required to access this resource")));
            }
            else {
                logger.debug(
                        "Access is denied (user is not anonymous); delegating to AccessDeniedHandler",
                        exception);

                accessDeniedHandler.handle(request, response,
                        (AccessDeniedException) exception);
            }
        }
    }

    protected void sendStartAuthentication(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain,
            AuthenticationException reason) throws ServletException, IOException {
        // SEC-112: Clear the SecurityContextHolder's Authentication, as the
        // existing Authentication is no longer considered valid
        SecurityContextHolder.getContext().setAuthentication(null);
        requestCache.saveRequest(request, response);   //保存当前请求
        logger.debug("Calling Authentication entry point.");
        authenticationEntryPoint.commence(request, response, reason);
    }

}
```

1. 如果抛出的异常是AuthenticationException，则执行方法sendStartAuthentication
2. 如果抛出的异常是AccessDeniedException，且从SecurityContextHolder.getContext().getAuthentication()得到的是AnonymousAuthenticationToken或者RememberMeAuthenticationToken，那么执行sendStartAuthentication
3. 如果上面的第二点不满足，则执行accessDeniedHandler的handle方法



在HttpSessionRequestCache 中会将本次请求的信息保存到session中

```java
public class HttpSessionRequestCache implements RequestCache {
    /**
     * Stores the current request, provided the configuration properties allow it.
     */
    public void saveRequest(HttpServletRequest request, HttpServletResponse response) {
        if (requestMatcher.matches(request)) {
            DefaultSavedRequest savedRequest = new DefaultSavedRequest(request,
                    portResolver);

            if (createSessionAllowed || request.getSession(false) != null) {
                // Store the HTTP request itself. Used by
                // AbstractAuthenticationProcessingFilter
                // for redirection after successful authentication (SEC-29)
                request.getSession().setAttribute(this.sessionAttrName, savedRequest);
                logger.debug("DefaultSavedRequest added to Session: " + savedRequest);
            }
        }
        else {
            logger.debug("Request not saved as configured RequestMatcher did not match");
        }
    }
}
```

```java
    public void setAccessDeniedHandler(AccessDeniedHandler accessDeniedHandler) {
        Assert.notNull(accessDeniedHandler, "AccessDeniedHandler required");
        this.accessDeniedHandler = accessDeniedHandler;
    }
```



#### ExceptionTranslationFilter的sendStartAuthentication方法

调用sendStartAuthentication方法实现对request的缓存和重定向

```java
    protected void sendStartAuthentication(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain,
            AuthenticationException reason) throws ServletException, IOException {
        // SEC-112: Clear the SecurityContextHolder's Authentication, as the
        // existing Authentication is no longer considered valid
        SecurityContextHolder.getContext().setAuthentication(null);
        requestCache.saveRequest(request, response);
        logger.debug("Calling Authentication entry point.");
        authenticationEntryPoint.commence(request, response, reason);
    }
```

在commence方法中完成对请求的重定向

```java
    public void commence(HttpServletRequest request, HttpServletResponse response,
            AuthenticationException authException) throws IOException, ServletException {

        String redirectUrl = null;

        if (useForward) {

            if (forceHttps && "http".equals(request.getScheme())) {
                // First redirect the current request to HTTPS.
                // When that request is received, the forward to the login page will be
                // used.
                redirectUrl = buildHttpsRedirectUrlForRequest(request);
            }

            if (redirectUrl == null) {
                String loginForm = determineUrlToUseForThisRequest(request, response,
                        authException);

                if (logger.isDebugEnabled()) {
                    logger.debug("Server side forward to: " + loginForm);
                }

                RequestDispatcher dispatcher = request.getRequestDispatcher(loginForm);

                dispatcher.forward(request, response);

                return;
            }
        }
        else {
            // redirect to login page. Use https if forceHttps true

            redirectUrl = buildRedirectUrlToLoginPage(request, response, authException);

        }

        redirectStrategy.sendRedirect(request, response, redirectUrl);
    }
```



#### 自定义未登录异常

如果未登录，不希望跳转到/login而是直接抛异常或跳转到指定路径，可以通过以下两步来实现：

1. 自定义类实现AuthenticationEntryPoint接口，重写commence方法。

   ```java
   @Configuration
   public class MyAuthenticationEntryPoint implements AuthenticationEntryPoint {
   
       @Override
       public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authException) throws IOException, ServletException {
           if (!response.isCommitted()) {
   //            response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED,"未认证的用户:" + authException.getMessage());
               new DefaultRedirectStrategy().sendRedirect(request, response, "http://www.jd.com");
           }
       }
   
   }
   ```

2. 在WebSecurityConfigurerAdapter继承类中指定异常处理类为自定义类。

   ```java
   @Configuration
   public class SecurityConfig extends WebSecurityConfigurerAdapter {
       @Override
       protected void configure(HttpSecurity http) throws Exception {
           http
                   //跨域请求伪造防御失效
                   .csrf().disable()
                   .authorizeRequests()
                   .antMatchers("/r/r1").hasAnyAuthority("p1")
                   .antMatchers("/uaa/publicKey", "/login**", "/isExpired**", "/mobile/**", "/check/**", "/user/**").permitAll()
                   .anyRequest().authenticated()
                   .and()
                   .formLogin()
                   .and()
                   .exceptionHandling()
                   .authenticationEntryPoint(new MyAuthenticationEntryPoint());
       }
   
       @Override
       protected void configure(AuthenticationManagerBuilder auth) throws Exception {
           super.configure(auth);
       }
   
       @Override
       public void configure(WebSecurity web) throws Exception {
           super.configure(web);
       }
   
   }
   ```

   

### 3.2.2 FilterSecurityInterceptor

在web应用中，spring security是一个filter。而在filter内部，它又自建了一个filter chain（如果不用命名空间，也可以自定义）。spring security按顺序对每个filter进行处理。各filter之间有较大的差异性。与权限验证关系最密切的是FilterSecurityInterceptor。

FilterSecurityInterceptor认证及验权流程：

![21580557-91f104e63676e03d.png](https://upload-images.jianshu.io/upload_images/21580557-804d34e60a6f7cf0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


FilterSecurityInterceptor的类关系图如下。它使用AuthenticationManager做认证（用户是否已登录），使用AccessDecisionManager做验证（用户是否有权限）。

![21580557-c3d28217250cf5ee.png](https://upload-images.jianshu.io/upload_images/21580557-b6c3735abaef297d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


ProviderManager是默认的AuthenticationManager实现类，它不直接进行认证。而是采用组合模式，将认证工作委托给AuthenticationProvider。一般情况下，一组AuthenticationProvider有一个认证成功，就被视为认证成功。ProviderManager关系图如下：

![21580557-18e1a04bf1e402e4.png](https://upload-images.jianshu.io/upload_images/21580557-313eb65e84dd4ed7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


AccessDecisionManager负责验证用户是否有操作权限，它也是采用组合模式。security自带的AccessDecisionManager实现类有三种：AffirmativeBased只要有一个认证处理器认证通过就表示成功；ConsensusBased采用的是多数原则；UnanimousBased采用一票否决制。

![21580557-eb6101754772e091.png](https://upload-images.jianshu.io/upload_images/21580557-33c6c54e66929cb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
