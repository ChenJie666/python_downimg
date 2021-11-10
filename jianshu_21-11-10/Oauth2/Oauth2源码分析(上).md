# 前言

**拦截器顺序：**

```
    FilterComparator() {
        int order = 100;
        put(ChannelProcessingFilter.class, ord![21580557-a1b4bb0cec787209.png](https://upload-images.jianshu.io/upload_images/21580557-064e10f042fb0e86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
er);
        order += STEP;
        put(ConcurrentSessionFilter.class, order);
        order += STEP;
        put(WebAsyncManagerIntegrationFilter.class, order);
        order += STEP;
        put(SecurityContextPersistenceFilter.class, order);
        order += STEP;
        put(HeaderWriterFilter.class, order);
        order += STEP;
        put(CorsFilter.class, order);
        order += STEP;
        put(CsrfFilter.class, order);
        order += STEP;
        put(LogoutFilter.class, order);
        order += STEP;
        filterToOrder.put(
            "org.springframework.security.oauth2.client.web.OAuth2AuthorizationRequestRedirectFilter",
            order);
        order += STEP;
        put(X509AuthenticationFilter.class, order);
        order += STEP;
        put(AbstractPreAuthenticatedProcessingFilter.class, order);
        order += STEP;
        filterToOrder.put("org.springframework.security.cas.web.CasAuthenticationFilter",
                order);
        order += STEP;
        filterToOrder.put(
            "org.springframework.security.oauth2.client.web.OAuth2LoginAuthenticationFilter",
            order);
        order += STEP;
        put(UsernamePasswordAuthenticationFilter.class, order);
        order += STEP;
        put(ConcurrentSessionFilter.class, order);
        order += STEP;
        filterToOrder.put(
                "org.springframework.security.openid.OpenIDAuthenticationFilter", order);
        order += STEP;
        put(DefaultLoginPageGeneratingFilter.class, order);
        order += STEP;
        put(ConcurrentSessionFilter.class, order);
        order += STEP;
        put(DigestAuthenticationFilter.class, order);
        order += STEP;
        put(BasicAuthenticationFilter.class, order);
        order += STEP;
        put(RequestCacheAwareFilter.class, order);
        order += STEP;
        put(SecurityContextHolderAwareRequestFilter.class, order);
        order += STEP;
        put(JaasApiIntegrationFilter.class, order);
        order += STEP;
        put(RememberMeAuthenticationFilter.class, order);
        order += STEP;
        put(AnonymousAuthenticationFilter.class, order);
        order += STEP;
        put(SessionManagementFilter.class, order);
        order += STEP;
        put(ExceptionTranslationFilter.class, order);
        order += STEP;
        put(FilterSecurityInterceptor.class, order);
        order += STEP;
        put(SwitchUserFilter.class, order);
    }
```

> 认证流程：Filter->构造Token->AuthenticationManager->转给Provider处理->认证处理成功后续操作或者不通过抛异常



**Security中的关键类：**

- ①UsernamePasswordAuthenticationFilter：如果是账号密码认证，从请求参数中获取账号密码，封装成为未认证过的UsernamePasswordAuthenticationToken对象，调用attemptAuthentication方法进行认证，在attemptAuthentication方法中会调用AuthenticationManager的authenticate方法对未认证的Authenticate对象token进行认证；
- ②UsernamePasswordAuthenticationToken：Authentication的子类，是验证方式的一种，有待验证和已验证两个构造方法。调用authenticate方法对其进行验证。principal参数的类型一般为UserDetails、String、AuthenticatedPrincipal、Principal；
- ③ProviderManager：在AuthenticationProvider的authenticate方法中会遍历AuthenticationProvider接口实现类的集合，遍历时会调用AuthenticationProvider实现类AbstractUserDetailsAuthenticationProvider的support方法判断需要验证的Authentication对象是否符合AuthenticationProvider的类型。直到support方法判断为true；
- ④AbstractUserDetailsAuthenticationProvider(AuthenticationProvider的实现类)：support方法为true，匹配上合适的AuthenticationProvider实现类后(UsernamePasswordAuthenticationToken匹配的是AbstractUserDetailsAuthenticationProvider抽象类)，调用AuthenticationProvider的authenticate方法进行验证(所以真正进行验证的是AuthenticationProvider实现类的authenticate方法)；
- ⑤DaoAuthenticationProvider(AuthenticationProvider和AbstractUserDetailsAuthenticationProvider的子类)：在authenticate方法中对Authentication对象token进行认证，取出对象中的username，在retrieveUser方法中调用UserDetailsService对象的loadUserByUsername(username)方法得到UserDetails对象，如果UserDetails对象不是null，则认证通过；最后调用继承自父类AbstractUserDetailsAuthenticationProvider的createSuccessAuthentication的方法，构建已认证的UsernamePasswordAuthenticationToken对象并返回。

> 构建已认证的UsernamePasswordAuthenticationToken对象并设置到上下文中SecurityContextHolder.getContext().setAuthentication(authenticationToken); 表示该请求已认证完成，后续安全拦截器放行。
> 构建已认证的UsernamePasswordAuthenticationToken的第三个参数是该用户所拥有的权限，后续的鉴权拦截器会根据传入的权限信息对请求进行鉴权。

![21580557-a1b4bb0cec787209.png](https://upload-images.jianshu.io/upload_images/21580557-928188d1c275d5f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**继承关系图**
![AuthenticationManager](https://upload-images.jianshu.io/upload_images/21580557-247d8132663f14c6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![21580557-069e9c62f9d5f45b.png](https://upload-images.jianshu.io/upload_images/21580557-4052f0837d2829fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




<br>
# 一、授权码模式源码

## 1.1 概述

**流程图：**

![1622700752041.png](https://upload-images.jianshu.io/upload_images/21580557-583da1bfe9c09fe9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




**框架默认提供的接口：**

- `AuthorizationEndpoint`   `/oauth/authorize`
- `WhitelabelApprovalEndpoint`   `/oauth/confirm_access`
- `TokenEndpoint`   `/oauth/token`
- `CheckTokenEndpoint`   `/oauth/check_token`
- `WhitelabelErrorEndpoint`   `/oauth/error`



**授权码模式和密码模式的部分区别：**

- 授权码模式输入账号密码通过`UsernamePasswordAuthenticationFilter`类的`attemptAuthentication`方法进行验证。
  授权码模式携带code请求令牌通过`ClientCredentialsTokenEndpointFilter`类的`attemptAuthentication`方法进行验证。
- 密码模式调用`ResourceOwnerPasswordTokenGranter`类的`getOAuth2Authentication`方法获取`OAuth2Authentication`;
  授权码模式调用`AuthorizationCodeTokenGranter`类的`getOAuth2Authentication`方法获取`OAuth2Authentication`;



**流程分析：**

访问认证服务器和资源服务器，需要第三方服务器已经注册到了认证服务器并生成了client_id和client_secret。

1. 以csdn为例，打开csdn登录页面，选择QQ登录。此时client为csdn，qq为authroization server和resouce server。qq授权服务器里存储了很多client信息，csdn只是众多client中的一个。
2. 携带response_type,client_id以及redirect_uri参数访问认证服务器，跳转到认证服务器的登录页面。用户填写用户名、密码后，点击授权并登录，首先访问qq授权服务器的/login路径，spring security验证username和password后给用户发放JSessionId的cookie，session中存储了Authentication。
3. 再访问qq授权服务器/oauth/authorize，请求参数有client_id、client_secret、grant_type、code、redirect_uri，验证通过后请求重定向到redirect_uri，且传递Authorization code。
4. redirect_uri路径指向的是client中的一个endpoint，client接收到了code，表明client信息已经在QQ授权服务器验证成功。再凭借这个code值外加client_id,client_secret,grant_type=authorization_code,code,redirect_uri等参数，去访问QQ的/oauth/token，返回access_token。
5. 获得access_token后，client再去找qq的资源服务器要资源。



**授权码模式流程的理解：**

`授权码模式获取授权码过程，其实就是访问接口/oauth/authorize来重定向到指定网址并携带授权码，但是该接口需要进行认证和鉴权（一般只要认证即可，如果只有部分用户可以使用授权码模式，可以给/oauth/authorize接口和用户设置权限），所以抛出异常重定向到用户登录页面进行用户登录和鉴权。如果客户端autoprove是false，会重定向到/oauth/confirm_access接口返回确认登录页面，点击确认携带user_oauth_approval（true）参数请求/oauth/authorize接口，最终携带授权码code重定向到指定页面。`



**各过滤器作用：**

- `UsernamePasswordAuthenticationFilter` => This filter by default responds to the URL {@code /login}.
- `OAuth2AuthenticationProcessingFilter` => 添加@EnableResourceServer注解就会自动添加该过滤器，用于解析和校验请求携带的token。



**Oauth框架源码比较奇怪的地方：**

1. 生成`freshToken`：先创建一个没有exp的，然后查询exp再创建有exp的`freshToken`覆盖最先生成的`freshToken`。
2. 验证`token：loadAuthentication`方法调用`readAccessToken`生成`OAuth2AccessToken`，`readAuthentication`方法调用`readAuthentication`生成`OAuth2Authentication`。连续调用了两次`JwtHelper`类的`decodeAndVerify`方法对`token`进行验证。



**关键类（校验令牌，生成令牌，令牌加强）**

Token令牌时遍历`List<AuthenticationProvider>`寻找合适的`AuthenticationProvider`；生成Token令牌时遍历`List<AuthorizationCodeTokenGranter>`寻找合适的`AuthorizationCodeTokenGranter`；加强Token令牌时遍历`List<TokenEnhancer>`寻找合适的 `TokenEnhancer` ，并调用`enhance`方法对`OAuth2AccessToken` 进行加强。



**总结：**

不管是请求`/oauth/authorize`还是`/oauth/token`，不管是授权码模式还是密码模式，都需要经过过滤器对用户账号密码或是客户端账号密码进行认证，然后到达接口进行业务处理（如获取授权码、获取令牌）。然后经过`ExceptionTranslationFilter`过滤器到达`FilterSecurityInterceptor`，对请求的认证信息和权限信息进行校验，如果校验不通过抛出异常到`FilterSecurityInterceptor`进行相应的处理（如重定向到/login页面）。



**异常处理**

如果授权未通过抛出异常，会在`ExceptionTrancationalFilter`类中处理，如果是`AccessDeniedException`异常且是匿名用户，会调用`AuthenticationEntryPoint`接口的`commence`方法进行后续处理。默认的是重定向到请求地址的`/login`页面进行登录，可以进行重写，实现重定向地址的改写或直接抛异常等功能。



## 1.2 源码

### 1.2.1 获取授权码流程

**流程：**

1. 请求<http://localhost:9500/oauth/authorize?client_id=c1&response_type=code&scope=ROLE_ADMIN&redirect_uri=http://www.taobao.com>，
   对client信息进行校验。校验通过后进行接口权限校验。
2. 因为/oauth/authorize未开放权限，所以用户需要鉴权。分两种情况，cookie中是否有用户信息：
   2.1 如果请求的cookie中有用户的账号密码，直接进行登录，并完成登录用户的鉴权，直接跳转到`/oauth/confirm_access`接口（`WhitelabelApprovalEndpoint`类），返回该类中拼接html代码，即确认授权页面。
   2.2 如果cookie中没有用户的账号密码，重定向到登录页面（缺省为/login）。点击login in后进行表单提交（默认提交地址为/login），通过`UsernamePasswordAuthenticationFilter`进行验证，验证通过后，继续请求资源地址<http://localhost:9500/oauth/authorize?client_id=c1&response_type=code&scope=ROLE_ADMIN&redirect_uri=http://www.taobao.com>。对客户端的账号密码等信息进行校验。然后跳转到/oauth/confirm_access接口(WhitelabelApprovalEndpoint类），返回该类中拼接html代码，即确认授权页面。
3. 同意授权后携带参数user_oauth_approval（true）请求<http://localhost:9500/oauth/authorize>，最终重定向到带有code的指定路径。

请求中会携带已认证的请求参数，在服务中的session中也存储请求信息。



#### ①首次请求/oauth/authorize

因为请求未经认证，直接跳过上述拦截器进入ExceptionTranslationFilter类中的，因为用户未进行认证是匿名用户，且未输入用户密码，抛出AccessDeniedException异常，进入handleSpringSecurityException方法，调用sendStartAuthentication方法，其中会将该次请求信息存储到session中requestCache.saveRequest(request, response)，然后
调用LoginUrlAuthenticationEntryPoint的commence方法，其中会调用redirectUrl = buildRedirectUrlToLoginPage(request, response, authException);得到redirectUrl="<http://localhost:9500/login>"，
并将重定向地址写入到response中 ，并将现请求路径存储到session的saverequest中。然后等到过滤器链走完后就会重定向到指定地址。

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
            // 得到重定向的地址redirectUrl="http://localhost:9500/login"
            redirectUrl = buildRedirectUrlToLoginPage(request, response, authException);

        }
        //跳转到重定向的地址
        redirectStrategy.sendRedirect(request, response, redirectUrl);
    }
```



#### ②用户密码登录

输入账号密码Sign in，且已输入用户密码，则将该次请求信息存储到session中，进入到UsernamePasswordAuthenticationFilter拦截器调用attemptAuthentication方法对账号密码进行验证。授权码模式最终会调用AbstractUserDetailsAuthenticationProvider类的authenticate方法对创建的未进行认证的UsernamePasswordAuthenticationToken进行认证。

```java
//UsernamePasswordAuthenticationFilter的attemptAuthentication方法
    public Authentication attemptAuthentication(HttpServletRequest request,
            HttpServletResponse response) throws AuthenticationException {
        if (postOnly && !request.getMethod().equals("POST")) {
            //不是POST方法，抛异常
            throw new AuthenticationServiceException(
                    "Authentication method not supported: " + request.getMethod());
        }
        //从请求中获取参数
        String username = obtainUsername(request);
        String password = obtainPassword(request);

        if (username == null) {
            username = "";
        }

        if (password == null) {
            password = "";
        }

        username = username.trim();
		// 我不知道用户名密码是不是对的，所以构造一个未认证的Token先
        UsernamePasswordAuthenticationToken authRequest = new UsernamePasswordAuthenticationToken(
                username, password);

        // 顺便把请求和Token存起来
        setDetails(request, authRequest);
		// Token给当前的AuthenticationManager处理
        return this.getAuthenticationManager().authenticate(authRequest);
    }
```

> 从请求参数中获取username和password，通过username和password构建一个未认证的UsernamePasswordAuthenticationToken，然后调用AuthenticationManager的authenticate方法进行认证。

```java
//AbstractUserDetailsAuthenticationProvider类的authenticate方法
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        Assert.isInstanceOf(UsernamePasswordAuthenticationToken.class, authentication,() -> messages.getMessage("AbstractUserDetailsAuthenticationProvider.onlySupports","Only UsernamePasswordAuthenticationToken is supported"));

        // 此处getPrincipal()为null，所以username为用户输入的用户名admin
        String username = (authentication.getPrincipal() == null) ? "NONE_PROVIDED" : authentication.getName();

        boolean cacheWasUsed = true;
        //缓存中没有UserDetails，所以user为null
        UserDetails user = this.userCache.getUserFromCache(username);

        if (user == null) {
            cacheWasUsed = false;

            try {
                //通过我们重写的loadUserByUsername方法获取UserDetails
                user = retrieveUser(username,(UsernamePasswordAuthenticationToken) authentication);
            } catch (UsernameNotFoundException notFound) {
                logger.debug("User '" + username + "' not found");

                if (hideUserNotFoundExceptions) {
                    throw new BadCredentialsException(messages.getMessage(
                            "AbstractUserDetailsAuthenticationProvider.badCredentials",
                            "Bad credentials"));
                }
                else {
                    throw notFound;
                }
            }

            Assert.notNull(user,
                    "retrieveUser returned null - a violation of the interface contract");
        }

        try {
            //检查isAccountNonLocked、isEnabled、isAccountNonExpired信息，如果为false则抛异常
            preAuthenticationChecks.check(user);
            //检查UserDetails中的密码和UsernamePasswordAuthenticationToken中的密码是否一致
            additionalAuthenticationChecks(user,(UsernamePasswordAuthenticationToken) authentication);
        }
        catch (AuthenticationException exception) {
            if (cacheWasUsed) {
                // There was a problem, so try again after checking
                // we're using latest data (i.e. not from the cache)
                cacheWasUsed = false;
                user = retrieveUser(username,
                        (UsernamePasswordAuthenticationToken) authentication);
                preAuthenticationChecks.check(user);
                additionalAuthenticationChecks(user,
                        (UsernamePasswordAuthenticationToken) authentication);
            }
            else {
                throw exception;
            }
        }
        //检查isCredentialsNonExpired信息，如果为false则抛异常
        postAuthenticationChecks.check(user);

        //将UserDetails放到缓存中
        if (!cacheWasUsed) {
            this.userCache.putUserInCache(user);
        }

        Object principalToReturn = user;
        //因为forcePrincipalAsString是false，所以principalToReturn 是UserDetails
        if (forcePrincipalAsString) {
            principalToReturn = user.getUsername();
        }

        return createSuccessAuthentication(principalToReturn, authentication, user);
    }
```

调用了上述类的子类DaoAuthenticationProvider的重写方法**retrieveUser**，在该方法中会调用我们重写的loadUserByUsername方法获取用户的UserDetails(包含password)，如果返回的UserDetails为null，则抛异常。

```java
//DaoAuthenticationProvider的retrieveUser方法
    protected final UserDetails retrieveUser(String username,
            UsernamePasswordAuthenticationToken authentication)
            throws AuthenticationException {
        prepareTimingAttackProtection();
        try {
            UserDetails loadedUser = this.getUserDetailsService().loadUserByUsername(username);
            if (loadedUser == null) {
                throw new InternalAuthenticationServiceException(
                        "UserDetailsService returned null, which is an interface contract violation");
            }
            return loadedUser;
        }
        catch (UsernameNotFoundException ex) {
            mitigateAgainstTimingAttack(authentication);
            throw ex;
        }
        catch (InternalAuthenticationServiceException ex) {
            throw ex;
        }
        catch (Exception ex) {
            throw new InternalAuthenticationServiceException(ex.getMessage(), ex);
        }
    }
```

验证密码会调用子类DaoAuthenticationProvider重写的方法additionalAuthenticationChecks，如果UserDetails中的password解码后与未认证的UsernamePasswordAuthenticationToken中的password不一致，抛BadCredentialsException异常。

```java
//DaoAuthenticationProvider类的additionalAuthenticationChecks
    protected void additionalAuthenticationChecks(UserDetails userDetails,
            UsernamePasswordAuthenticationToken authentication)
            throws AuthenticationException {
        if (authentication.getCredentials() == null) {
            logger.debug("Authentication failed: no credentials provided");

            throw new BadCredentialsException(messages.getMessage(
                    "AbstractUserDetailsAuthenticationProvider.badCredentials",
                    "Bad credentials"));
        }

        String presentedPassword = authentication.getCredentials().toString();

        if (!passwordEncoder.matches(presentedPassword, userDetails.getPassword())) {
            logger.debug("Authentication failed: password does not match stored value");

            throw new BadCredentialsException(messages.getMessage(
                    "AbstractUserDetailsAuthenticationProvider.badCredentials",
                    "Bad credentials"));
        }
    }
```

最后将UserDetails(principal)、未认证的UsernamePasswordAuthenticationToken和UserDetails作为参数调用父类AbstractUserDetailsAuthenticationProvider的createSuccessAuthentication方法，最终调用得到，得到已认证的UsernamePasswordAuthenticationToken。

```java
//AbstractUserDetailsAuthenticationProvider的createSuccessAuthentication方法
    protected Authentication createSuccessAuthentication(Object principal,
            Authentication authentication, UserDetails user) {
        // Ensure we return the original credentials the user supplied,
        // so subsequent attempts are successful even with encoded passwords.
        // Also ensure we return the original getDetails(), so that future
        // authentication events after cache expiry contain the details
        UsernamePasswordAuthenticationToken result = new UsernamePasswordAuthenticationToken(
                principal, authentication.getCredentials(),
                authoritiesMapper.mapAuthorities(user.getAuthorities()));
        result.setDetails(authentication.getDetails());

        return result;
    }
```



**最后得到已认证的UsernamePasswordAuthenticationToken**，将其添加到请求的参数中(Map<String, Object> model, @RequestParam Map<String, String> parameters,
SessionStatus sessionStatus, Principal principal)

![21580557-2af07faffc4711cb.png](https://upload-images.jianshu.io/upload_images/21580557-f02441fa2725616b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


验证通过后执行successHandler.onAuthenticationSuccess(request, response, authResult)，获取session中的savedrequest，重定向到原先的地址/oauth/authorize，并附带完整请求参数。

```java
public class SavedRequestAwareAuthenticationSuccessHandler extends
        SimpleUrlAuthenticationSuccessHandler {
    protected final Log logger = LogFactory.getLog(this.getClass());
 
    private RequestCache requestCache = new HttpSessionRequestCache();
 
    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
            HttpServletResponse response, Authentication authentication)
            throws ServletException, IOException {
             // HttpSessionRequestCache.getRequest ,找名为SPRING_SECURITY_SAVED_REQUEST的session
        SavedRequest savedRequest = requestCache.getRequest(request, response);
 
        if (savedRequest == null) {
            super.onAuthenticationSuccess(request, response, authentication);
 
            return;
        }
        String targetUrlParameter = getTargetUrlParameter();
        if (isAlwaysUseDefaultTargetUrl()
                || (targetUrlParameter != null && StringUtils.hasText(request
                        .getParameter(targetUrlParameter)))) {
            requestCache.removeRequest(request, response);
            super.onAuthenticationSuccess(request, response, authentication);
 
            return;
        }
 
        clearAuthenticationAttributes(request);
 
        // Use the DefaultSavedRequest URL
           // 获得原先存储在SavedRequest中的redirectUrl,即/oauth/authorize
        String targetUrl = savedRequest.getRedirectUrl();
        logger.debug("Redirecting to DefaultSavedRequest Url: " + targetUrl);
        getRedirectStrategy().sendRedirect(request, response, targetUrl);
    }
 
    public void setRequestCache(RequestCache requestCache) {
        this.requestCache = requestCache;
    }
}
```

在ProviderManager中通过eraseCredentials方法将UsernamePasswordAuthenticationToken中的所有密码删除()，然后通过publishAuthenticationSuccess方法将发布认证成功事件。

如果验证过程没有抛出异常，最后会再次进入ExceptionTranslationFilter类中，用于接收FilterSecurityInterceptor拦截器抛出的异常。如果没有抛出异常，那么正常访问/oauth/authorize接口。
进入AuthorizationEndpoint类(接口类)的authorize方法中(/oauth/authorize接口)，对client信息进行验证(包括有效性、scope、重定向地址等)。如果客户端已经预授权，直接生成code(将code和序列化后的OAuth2Authentication存储到数据库)并重定向到指定地址；如果客户端未预授权，则重定向到确认授权页面。

```java
    @RequestMapping(value = "/oauth/authorize")
    public ModelAndView authorize(Map<String, Object> model, @RequestParam Map<String, String> parameters,
            SessionStatus sessionStatus, Principal principal) {

        // 通过Oauth2RequestFactory构建AuthorizationRequest
        AuthorizationRequest authorizationRequest = getOAuth2RequestFactory().createAuthorizationRequest(parameters);

        Set<String> responseTypes = authorizationRequest.getResponseTypes();

        //oauth/authorize这个请求只支持授权码code模式和Implicit隐式模式
        if (!responseTypes.contains("token") && !responseTypes.contains("code")) {
            throw new UnsupportedResponseTypeException("Unsupported response types: " + responseTypes);
        }

        if (authorizationRequest.getClientId() == null) {
            throw new InvalidClientException("A client id must be provided");
        }

        try {
            //验证请求中的携带的身份信息principal 是否已经验证
            if (!(principal instanceof Authentication) || !((Authentication) principal).isAuthenticated()) {
                throw new InsufficientAuthenticationException(
                        "User must be authenticated with Spring Security before authorization can be completed.");
            }
            //通过ClientDetailsService检索ClientDetails
            ClientDetails client = getClientDetailsService().loadClientByClientId(authorizationRequest.getClientId());
            //获取重定向的地址
            String redirectUriParameter = authorizationRequest.getRequestParameters().get(OAuth2Utils.REDIRECT_URI);
            String resolvedRedirect = redirectResolver.resolveRedirect(redirectUriParameter, client);
            //确保requst中有重定向redirect_uri
            if (!StringUtils.hasText(resolvedRedirect)) {
                throw new RedirectMismatchException(
                        "A redirectUri must be either supplied or preconfigured in the ClientDetails");
            }
            //设置重定向地址
            authorizationRequest.setRedirectUri(resolvedRedirect);

            // 校验client请求的是一组有效的scope,通过比对表oauth_client_details
            oauth2RequestValidator.validateScope(authorizationRequest, client);

            //预同意处理(ApprovalStoreUserApprovalHandler)
            //1. 校验所有的scope是否已经全部是自动同意授权，如果全部自动授权同意，则设置authorizationRequest
            //中属性approved为true,否则走2
            //2. 查询client_id下所有oauth_approvals，校验在有效时间内Scope授权的情况，如果在有效时间内Scope授权全部同意，
            //则设置authorizationRequest中属性approved为true,否则为false
            authorizationRequest = userApprovalHandler.checkForPreApproval(authorizationRequest,
                    (Authentication) principal);
            // TODO: is this call necessary?
            // 这个步骤是不是多余的？？
            boolean approved = userApprovalHandler.isApproved(authorizationRequest, (Authentication) principal);
            authorizationRequest.setApproved(approved);

            // 如果预授权参数是true，直接将code重定向到redirect_uri
            if (authorizationRequest.isApproved()) {
                if (responseTypes.contains("token")) {
                    return getImplicitGrantResponse(authorizationRequest);
                }
                if (responseTypes.contains("code")) {
                    return new ModelAndView(getAuthorizationCodeResponse(authorizationRequest,
                            (Authentication) principal));
                }
            }

            //如果预授权参数是false，跳转到授权页面
            //授权页面是由WhitelabelApprovalEndpoint类生成的
            return getUserApprovalPageResponse(model, authorizationRequest, (Authentication) principal);

        }
        catch (RuntimeException e) {
            sessionStatus.setComplete();
            throw e;
        }

    }
```

如果未进行预授权，则将认证信息添加到response中并会重定向到确认授权页面，代码如下。

```java
    private String userApprovalPage = "forward:/oauth/confirm_access";
    private ModelAndView getUserApprovalPageResponse(Map<String, Object> model,
            AuthorizationRequest authorizationRequest, Authentication principal) {
        if (logger.isDebugEnabled()) {
            logger.debug("Loading user approval page: " + userApprovalPage);
        }
        model.putAll(userApprovalHandler.getUserApprovalRequest(authorizationRequest, principal));
                //userApprovalPage为重定向地址：/oauth/confirm_access
        return new ModelAndView(userApprovalPage, model);
    }
```

同意授权后会携带授权信息并再次进入过滤器链，并携带code重定向到指定的地址。



### 1.2.2 请求token流程

#### ①验证客户端信息

概述：此处的源码流程与请求相同，只是授权码模式已经完成了账号密码的验证，只需要将其换成client的账号密码即可。

访问localhost:9500/oauth/token?client_id=c1&client_secret=123456&grant_type=authorization_code&code=8bhrYC&redirect_uri=http://www.taobao.com。
先进入AbstractAuthenticationProcessingFilter的doFilter方法中，调用其实现类ClientCredentialsTokenEndpointFilter的attemptAuthentication方法进行验证。主要是对client的信息进行验证，通过clientId和clientSecret构建未认证的UsernamePasswordAuthenticationToken对象，调用authenticate方法对其进行认证。

```java
//ClientCredentialsTokenEndpointFilter类的attemptAuthentication方法
	@Override
	public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response)
			throws AuthenticationException, IOException, ServletException {

		if (allowOnlyPost && !"POST".equalsIgnoreCase(request.getMethod())) {
			throw new HttpRequestMethodNotSupportedException(request.getMethod(), new String[] { "POST" });
		}

		String clientId = request.getParameter("client_id");
		String clientSecret = request.getParameter("client_secret");

		// If the request is already authenticated we can assume that this
		// filter is not needed
		Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
		if (authentication != null && authentication.isAuthenticated()) {
			return authentication;
		}

		if (clientId == null) {
			throw new BadCredentialsException("No client credentials presented");
		}

		if (clientSecret == null) {
			clientSecret = "";
		}

		clientId = clientId.trim();
		UsernamePasswordAuthenticationToken authRequest = new UsernamePasswordAuthenticationToken(clientId,
				clientSecret);

		return this.getAuthenticationManager().authenticate(authRequest);

	}
```

在ProviderManager类的authentication方法中对AuthenticationProvider列表进行遍历，直到获得可以匹配传入的UsernamePasswordAuthenticationToken类的AuthenticationProvider类，即DaoAuthenticationProvider。

```java
//ProviderManager类的authentication方法
	public Authentication authenticate(Authentication authentication)
			throws AuthenticationException {
		Class<? extends Authentication> toTest = authentication.getClass();
		AuthenticationException lastException = null;
		AuthenticationException parentException = null;
		Authentication result = null;
		Authentication parentResult = null;
		boolean debug = logger.isDebugEnabled();

		for (AuthenticationProvider provider : getProviders()) {
			if (!provider.supports(toTest)) {
				continue;
			}

			if (debug) {
				logger.debug("Authentication attempt using "
						+ provider.getClass().getName());
			}

			try {
				result = provider.authenticate(authentication);

				if (result != null) {
					copyDetails(authentication, result);
					break;
				}
			}
			catch (AccountStatusException | InternalAuthenticationServiceException e) {
				prepareException(e, authentication);
				throw e;
			} catch (AuthenticationException e) {
				lastException = e;
			}
		}

		if (result != null) {
			if (eraseCredentialsAfterAuthentication
					&& (result instanceof CredentialsContainer)) {
				// Authentication is complete. Remove credentials and other secret data
				// from authentication
				((CredentialsContainer) result).eraseCredentials();
			}

			// If the parent AuthenticationManager was attempted and successful than it will publish an AuthenticationSuccessEvent
			// This check prevents a duplicate AuthenticationSuccessEvent if the parent AuthenticationManager already published it
			if (parentResult == null) {
				eventPublisher.publishAuthenticationSuccess(result);
			}
			return result;
		}

        ......

    }
```

同样调用AbstractUserDetailsAuthenticationProvider的authenticate方法。

```java
	public Authentication authenticate(Authentication authentication)
			throws AuthenticationException {
		Assert.isInstanceOf(UsernamePasswordAuthenticationToken.class, authentication,
				() -> messages.getMessage(
						"AbstractUserDetailsAuthenticationProvider.onlySupports",
						"Only UsernamePasswordAuthenticationToken is supported"));

		// Determine username
		String username = (authentication.getPrincipal() == null) ? "NONE_PROVIDED"
				: authentication.getName();

		boolean cacheWasUsed = true;
		UserDetails user = this.userCache.getUserFromCache(username);

		if (user == null) {
			cacheWasUsed = false;

			try {
				user = retrieveUser(username,
						(UsernamePasswordAuthenticationToken) authentication);
			}
			catch (UsernameNotFoundException notFound) {
				logger.debug("User '" + username + "' not found");

				if (hideUserNotFoundExceptions) {
					throw new BadCredentialsException(messages.getMessage(
							"AbstractUserDetailsAuthenticationProvider.badCredentials",
							"Bad credentials"));
				}
				else {
					throw notFound;
				}
			}

			Assert.notNull(user,
					"retrieveUser returned null - a violation of the interface contract");
		}

		try {
			preAuthenticationChecks.check(user);
			additionalAuthenticationChecks(user,
					(UsernamePasswordAuthenticationToken) authentication);
		}
		catch (AuthenticationException exception) {
			if (cacheWasUsed) {
				// There was a problem, so try again after checking
				// we're using latest data (i.e. not from the cache)
				cacheWasUsed = false;
				user = retrieveUser(username,
						(UsernamePasswordAuthenticationToken) authentication);
				preAuthenticationChecks.check(user);
				additionalAuthenticationChecks(user,
						(UsernamePasswordAuthenticationToken) authentication);
			}
			else {
				throw exception;
			}
		}

		postAuthenticationChecks.check(user);

		if (!cacheWasUsed) {
			this.userCache.putUserInCache(user);
		}

		Object principalToReturn = user;

		if (forcePrincipalAsString) {
			principalToReturn = user.getUsername();
		}

		return createSuccessAuthentication(principalToReturn, authentication, user);
	}
```

区别在于retrieveUser时注入的是ClientDetailsUserDetailsService对象，调用loadUserByUsername方法，查询的是client表，获取到client的信息。返回的是User对象，该对象自动将check方法检查的属性全部置为true。

```java
//User类继承自UserDetails
public class User implements UserDetails, CredentialsContainer {
	public User(String username, String password,
			Collection<? extends GrantedAuthority> authorities) {
		this(username, password, true, true, true, true, authorities);
	}
}
```

同样的通过additionalAuthenticationChecks方法检查client的密码是否正确。并进行缓存。
所有校验都通过后，调用 createSuccessAuthentication() 返回认证信息。

```java
//AbstractUserDetailsAuthenticationProvider的createSuccessAuthentication方法
	protected Authentication createSuccessAuthentication(Object principal,
			Authentication authentication, UserDetails user) {
		//创建已认证的UsernamePasswordAuthenticationToken
		UsernamePasswordAuthenticationToken result = new UsernamePasswordAuthenticationToken(
				principal, authentication.getCredentials(),
				authoritiesMapper.mapAuthorities(user.getAuthorities()));
		result.setDetails(authentication.getDetails());

		return result;
	}
```

在该方法中创建已认证的UsernamePasswordAuthenticationToken（将authenticated属性设置为true），并设置UserDetails后返回。
在ProviderManager类的eraseCredentials方法中将credentials置为null后返回到AbstractAuthenticationProcessingFilter类的dofilter方法中。
最后调用AbstractAuthenticationProcessingFilter的successfulAuthentication方法。

```java
//ClientCredentialsTokenEndpointFilter的successfulAuthentication方法
	@Override
	protected void successfulAuthentication(HttpServletRequest request, HttpServletResponse response,
			FilterChain chain, Authentication authResult) throws IOException, ServletException {
		super.successfulAuthentication(request, response, chain, authResult);
		chain.doFilter(request, response);
	}
```

在其父类的successfulAuthentication方法中将已认证的UsernamePasswordAuthenticationToken**放置到安全上下文中**。

```java
//ClientCredentialsTokenEndpointFilter的父类AbstractAuthenticationProcessingFilter的successfulAuthentication方法
	protected void successfulAuthentication(HttpServletRequest request,
			HttpServletResponse response, FilterChain chain, Authentication authResult)
			throws IOException, ServletException {

		if (logger.isDebugEnabled()) {
			logger.debug("Authentication success. Updating SecurityContextHolder to contain: "
					+ authResult);
		}

		SecurityContextHolder.getContext().setAuthentication(authResult);

		rememberMeServices.loginSuccess(request, response, authResult);

		// Fire event
		if (this.eventPublisher != null) {
			eventPublisher.publishEvent(new InteractiveAuthenticationSuccessEvent(
					authResult, this.getClass()));
		}

		successHandler.onAuthenticationSuccess(request, response, authResult);
	}
```

最后调用下一级过滤器。因为已经设置到安全上下文中，所以过滤器放行，请求最终到达TokenEndpoint类的/oauth/token接口中。



#### ②生成token流程

![21580557-a5e7032d24362bbc.png](https://upload-images.jianshu.io/upload_images/21580557-8e83b772032894c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


在TokenPoint类的postAccessToken方法(/oauth/token接口)中进行client校验和令牌获取。
大致流程如下：
从 principal 中获取 clientId, 进而装载 ClientDetails 。
从 parameters 中获取 clientId、scope、grantType 以组装 TokenRequest。
校验 Client 信息。
根据 grantType 设置 TokenRequest 的 scope。
通过令牌授予者获取 Token。

```java
@FrameworkEndpoint
public class TokenEndpoint extends AbstractEndpoint {
    // 以下是核心部分代码...
    @RequestMapping(value = "/oauth/token", method=RequestMethod.POST)
    public ResponseEntity<OAuth2AccessToken> postAccessToken(Principal principal, @RequestParam Map<String, String> parameters) throws HttpRequestMethodNotSupportedException {

        if (!(principal instanceof Authentication)) {
            throw new InsufficientAuthenticationException(
                    "There is no client authentication. Try adding an appropriate authentication filter.");
        }

        // 1. 从 principal 中获取 clientId, 进而 load client 信息
        String clientId = getClientId(principal);
        ClientDetails authenticatedClient = getClientDetailsService().loadClientByClientId(clientId);

        // 2. 从 parameters 中拿 clientId、scope、grantType 组装 TokenRequest
        TokenRequest tokenRequest = getOAuth2RequestFactory().createTokenRequest(parameters, authenticatedClient);

        // 3. 校验 client 信息
        if (clientId != null && !clientId.equals("")) {
            if (!clientId.equals(tokenRequest.getClientId())) {
                // 双重校验: 确保从 principal 拿到的 client 信息与根据 parameters 得到的 client 信息一致
                throw new InvalidClientException("Given client ID does not match authenticated client");
            }
        }
        if (authenticatedClient != null) {
            oAuth2RequestValidator.validateScope(tokenRequest, authenticatedClient);
        }

        // 4. 根据 grantType 设置 TokenRequest 的 scope。
        // 授权类型有: password 模式、authorization_code 模式、refresh_token 模式、client_credentials 模式、implicit 模式
        if (!StringUtils.hasText(tokenRequest.getGrantType())) {
            throw new InvalidRequestException("Missing grant type");
        }
        if (tokenRequest.getGrantType().equals("implicit")) {
            throw new InvalidGrantException("Implicit grant type not supported from token endpoint");
        }

        // 如果是授权码模式, 则清空从数据库查询到的 scope。 因为授权请求过程会确定 scope, 所以没必要传。
        if (isAuthCodeRequest(parameters)) {
            if (!tokenRequest.getScope().isEmpty()) {
                logger.debug("Clearing scope of incoming token request");
                tokenRequest.setScope(Collections.<String> emptySet());
            }
        }

        // 如果是刷新 Token 模式, 解析并设置 scope
        if (isRefreshTokenRequest(parameters)) {
			// A refresh token has its own default scopes, so we should ignore any added by the factory here.
            tokenRequest.setScope(OAuth2Utils.parseParameterList(parameters.get(OAuth2Utils.SCOPE)));
        }

        // 5. 通过令牌授予者获取 token
        OAuth2AccessToken token = getTokenGranter().grant(tokenRequest.getGrantType(), tokenRequest);
        if (token == null) {
            throw new UnsupportedGrantTypeException("Unsupported grant type: " + tokenRequest.getGrantType());
        }

        return getResponse(token);
    }
    // ...
}
```

通过getTokenGranter方法获取AuthorizationServerEndpointsConfigurer，以tokenRequest作为参数，调用grant方法获取token。![21580557-6d771ccaf22d5b64.png](https://upload-images.jianshu.io/upload_images/21580557-5af2ff98ce884def.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


以下是各授权模式对应的 TokenGranter:

| 实现类                            | 对应的授权模式  |
| --------------------------------- | --------------- |
| AuthorizationCodeTokenGranter     | 授权码模式      |
| ClientCredentialsTokenGranter     | 客户端模式      |
| ImplicitTokenGranter              | implicit 模式   |
| RefreshTokenGranter               | 刷新 token 模式 |
| ResourceOwnerPasswordTokenGranter | 密码模式        |

```java
//AuthorizationServerEndpointsConfigurer中的getTokenGranter和grant方法
 	public TokenGranter getTokenGranter() {
		return tokenGranter();
	}

	private TokenGranter tokenGranter() {
		if (tokenGranter == null) {
			tokenGranter = new TokenGranter() {
				private CompositeTokenGranter delegate;

				@Override
				public OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest) {
					if (delegate == null) {
						delegate = new CompositeTokenGranter(getDefaultTokenGranters());
					}
					return delegate.grant(grantType, tokenRequest);
				}
			};
		}
		return tokenGranter;
	}
```

疑问：为什么TokenEndpoint中的getTokenGranter方法会调用AuthorizationServerEndpointsConfigurer中的getTokenGranter方法。

最终调用了AuthorizationServerEndpointsConfigurer中的TokenGranter的grant方法。在该方法中调用了CompositeTokenGranter类的grant方法，CompositeTokenGranter的属性List<TokenGranter>中包含了如下5种授权模式。
![21580557-b82d8d36e87a0293.png](https://upload-images.jianshu.io/upload_images/21580557-2f9138716cab8b49.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```java
//CompositeTokenGranter类的grant方法
	public OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest) {
		for (TokenGranter granter : tokenGranters) {
			OAuth2AccessToken grant = granter.grant(grantType, tokenRequest);
			if (grant!=null) {
				return grant;
			}
		}
		return null;
	}
```

同验证Token令牌时遍历List<AuthenticationProvider>寻找合适的AuthenticationProvider一样，此处也会寻找合适的TokenGranter，调用grant方法返回生成的OAuth2AccessToken。其子类继承了grant方法，判断每个子类的grantType属性是否和请求的grantType一致，最终匹配到**AuthorizationCodeTokenGranter**。
>**AuthorizationServerConfigurerAdapter类的三个重载方法的配置参数**
>- ClientDetailsServiceConfigurer：用来配置客户端详情服务，客户端详情信息在这里进行初始化，可以把客户端详情信息写死在这里或者通过数据库来存储调取详情信息。
>- AuthorizationServerEndpointsConfigurer：用来配置令牌（token） 的访问端点和令牌服务（token services）。
>- AuthorizationServerSecurityConfigurer：用来配置令牌端点的安全约束（权限）。

```java
//AbstractTokenGranter类的grant，getAccessToken和方法
	public OAuth2AccessToken grant(String grantType, TokenRequest tokenRequest) {

		if (!this.grantType.equals(grantType)) {
			return null;
		}
		
		String clientId = tokenRequest.getClientId();
		ClientDetails client = clientDetailsService.loadClientByClientId(clientId);
		validateGrantType(grantType, client);

		if (logger.isDebugEnabled()) {
			logger.debug("Getting access token for: " + clientId);
		}

		return getAccessToken(client, tokenRequest);

	}

	protected OAuth2AccessToken getAccessToken(ClientDetails client, TokenRequest tokenRequest) {
		return tokenServices.createAccessToken(getOAuth2Authentication(client, tokenRequest));
	}
```

createAccessToken方法的参数是OAuth2Authentication，通过getOAuth2Authentication方法获得，AuthorizationCodeTokenGranter重写了父类的该方法。该方法中获取参数中的授权码和生成授权码时的客户端信息，然后删除数据库中的授权码，返回生成授权码时的客户端信息（即authentication）构成的OAuth2Authentication。对请求的客户端信息和生成授权码的客户端信息进行校验。

![21580557-dc4f99bbd915c5e7.png](https://upload-images.jianshu.io/upload_images/21580557-f2cb0760107073e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```java
//AuthorizationCodeTokenGranter类的getOAuth2Authentication方法。
	@Override
	protected OAuth2Authentication getOAuth2Authentication(ClientDetails client, TokenRequest tokenRequest) {

		Map<String, String> parameters = tokenRequest.getRequestParameters();
		String authorizationCode = parameters.get("code");
		String redirectUri = parameters.get(OAuth2Utils.REDIRECT_URI);

		if (authorizationCode == null) {
			throw new InvalidRequestException("An authorization code must be supplied.");
		}

		OAuth2Authentication storedAuth = authorizationCodeServices.consumeAuthorizationCode(authorizationCode);
		if (storedAuth == null) {
			throw new InvalidGrantException("Invalid authorization code: " + authorizationCode);
		}

		OAuth2Request pendingOAuth2Request = storedAuth.getOAuth2Request();
		// https://jira.springsource.org/browse/SECOAUTH-333
		// This might be null, if the authorization was done without the redirect_uri parameter
		String redirectUriApprovalParameter = pendingOAuth2Request.getRequestParameters().get(
				OAuth2Utils.REDIRECT_URI);

		if ((redirectUri != null || redirectUriApprovalParameter != null)
				&& !pendingOAuth2Request.getRedirectUri().equals(redirectUri)) {
			throw new RedirectMismatchException("Redirect URI mismatch.");
		}

		String pendingClientId = pendingOAuth2Request.getClientId();
		String clientId = tokenRequest.getClientId();
		if (clientId != null && !clientId.equals(pendingClientId)) {
			// just a sanity check.
			throw new InvalidClientException("Client ID mismatch");
		}

		// Secret is not required in the authorization request, so it won't be available
		// in the pendingAuthorizationRequest. We do want to check that a secret is provided
		// in the token request, but that happens elsewhere.

		Map<String, String> combinedParameters = new HashMap<String, String>(pendingOAuth2Request
				.getRequestParameters());
		// Combine the parameters adding the new ones last so they override if there are any clashes
		combinedParameters.putAll(parameters);
		
		// Make a new stored request with the combined parameters
		OAuth2Request finalStoredOAuth2Request = pendingOAuth2Request.createOAuth2Request(combinedParameters);
		
		Authentication userAuth = storedAuth.getUserAuthentication();
		
		return new OAuth2Authentication(finalStoredOAuth2Request, userAuth);

	}
```

返回的OAuth2Authentication作为参数，调用AuthorizationServerTokenServices的子类DefaultTokenServices的createAccessToken方法生成OAuth2AccessToken。该方法使用了tokenStore.getAccessToken(authentication)来获取的token。如果getAccessToken返回的token是null，则直接创建新的token；如果getAccessToken返回了持久化的token，则判断token是否过期，如果未过期则根据OAuth2Authentication 信息重新存储token以防信息变更，如果已过期则

```java
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

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints
                .authenticationManager(authenticationManager)//认证管理器
                .authorizationCodeServices(authorizationCodeServices)//授权码服务
                .tokenServices(tokenServices()) //令牌管理服务（设置令牌存储方式和令牌类型JWT）
                .allowedTokenEndpointRequestMethods(HttpMethod.POST);
    }
```

```java
//DefaultTokenServices的createAccessToken方法。其中TokenStore为配置的JwtTokenStore。
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

		// Only create a new refresh token if there wasn't an existing one
		// associated with an expired access token.
		// Clients might be holding existing refresh tokens, so we re-use it in
		// the case that the old access token
		// expired.
		if (refreshToken == null) {
			refreshToken = createRefreshToken(authentication);
		}
		// But the refresh token itself might need to be re-issued if it has
		// expired.
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

	//创建accessToken
	private OAuth2AccessToken createAccessToken(OAuth2Authentication authentication, OAuth2RefreshToken refreshToken) {
		DefaultOAuth2AccessToken token = new DefaultOAuth2AccessToken(UUID.randomUUID().toString());
		int validitySeconds = getAccessTokenValiditySeconds(authentication.getOAuth2Request());
		if (validitySeconds > 0) {
			token.setExpiration(new Date(System.currentTimeMillis() + (validitySeconds * 1000L)));
		}
		token.setRefreshToken(refreshToken);
		token.setScope(authentication.getOAuth2Request().getScope());

		return accessTokenEnhancer != null ? accessTokenEnhancer.enhance(token, authentication) : token;
	}

	//创建refreshToken
	private OAuth2RefreshToken createRefreshToken(OAuth2Authentication authentication) {
		if (!isSupportRefreshToken(authentication.getOAuth2Request())) {
			return null;
		}
		int validitySeconds = getRefreshTokenValiditySeconds(authentication.getOAuth2Request());
		String value = UUID.randomUUID().toString();
		if (validitySeconds > 0) {
			return new DefaultExpiringOAuth2RefreshToken(value, new Date(System.currentTimeMillis()
					+ (validitySeconds * 1000L)));
		}
		return new DefaultOAuth2RefreshToken(value);
	}
```

这个tokenStore具体是哪个实现类的对象，还要看我们在认证服务器(即继承了AuthorizationServerConfigurerAdapter类)，如果是Jwt，则直接返回null，重新创建token；如果是其他，则会获取该用户缓存的token并返回，不会创建新的token。

```java
//JwtTokenStore的getAccessToken方法
	@Override
	public OAuth2AccessToken getAccessToken(OAuth2Authentication authentication) {
		// We don't want to accidentally issue a token, and we have no way to reconstruct the refresh token
		return null;
	}
```

在DefaultTokenServices的createAccessToken方法中创建DefaultOAuth2AccessToken 并将expiration、refreshToken、scopes等信息存储到其中，得到如下token：

![21580557-9cd5c457adbf8c4e.png](https://upload-images.jianshu.io/upload_images/21580557-13d02d39bf1bcb04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


在最后会通过accessTokenEnhancer的enhance方法对该token进行强化

```java
public class TokenEnhancerChain implements TokenEnhancer {

	private List<TokenEnhancer> delegates = Collections.emptyList();

	/**
	 * @param delegates the delegates to set
	 */
	public void setTokenEnhancers(List<TokenEnhancer> delegates) {
		this.delegates = delegates;
	}

	/**
	 * Loop over the {@link #setTokenEnhancers(List) delegates} passing the result into the next member of the chain.
	 */
	public OAuth2AccessToken enhance(OAuth2AccessToken accessToken, OAuth2Authentication authentication) {
		OAuth2AccessToken result = accessToken;
		for (TokenEnhancer enhancer : delegates) {
			result = enhancer.enhance(result, authentication);
		}
		return result;
	}
}
```

此处同验证Token令牌时遍历List<AuthenticationProvider>寻找合适的AuthenticationProvider和生成Token令牌时遍历List<AuthorizationCodeTokenGranter>寻找合适的AuthorizationCodeTokenGranter。此处也会遍历List<TokenEnhancer>寻找合适的 TokenEnhancer ，并调用enhance方法对OAuth2AccessToken 进行加强。此处List<TokenEnhancer>只有一个元素，即**JwtAccessTokenConverter**。enhance方法添加jti（将value作为jti）、更改了value和refreshToken。

```java
//JwtAccessTokenConverter类的enhance方法
	public OAuth2AccessToken enhance(OAuth2AccessToken accessToken, OAuth2Authentication authentication) {
		DefaultOAuth2AccessToken result = new DefaultOAuth2AccessToken(accessToken);
		Map<String, Object> info = new LinkedHashMap<String, Object>(accessToken.getAdditionalInformation());
		String tokenId = result.getValue();
		if (!info.containsKey(TOKEN_ID)) {
			info.put(TOKEN_ID, tokenId);
		}
		else {
			tokenId = (String) info.get(TOKEN_ID);
		}
		result.setAdditionalInformation(info);
		result.setValue(encode(result, authentication));
		OAuth2RefreshToken refreshToken = result.getRefreshToken();
		if (refreshToken != null) {
			DefaultOAuth2AccessToken encodedRefreshToken = new DefaultOAuth2AccessToken(accessToken);
			encodedRefreshToken.setValue(refreshToken.getValue());
			// Refresh tokens do not expire unless explicitly of the right type
			encodedRefreshToken.setExpiration(null);
			try {
				Map<String, Object> claims = objectMapper
						.parseMap(JwtHelper.decode(refreshToken.getValue()).getClaims());
				if (claims.containsKey(TOKEN_ID)) {
					encodedRefreshToken.setValue(claims.get(TOKEN_ID).toString());
				}
			}
			catch (IllegalArgumentException e) {
			}
			Map<String, Object> refreshTokenInfo = new LinkedHashMap<String, Object>(
					accessToken.getAdditionalInformation());
			refreshTokenInfo.put(TOKEN_ID, encodedRefreshToken.getValue());
			refreshTokenInfo.put(ACCESS_TOKEN_ID, tokenId);
			encodedRefreshToken.setAdditionalInformation(refreshTokenInfo);
			DefaultOAuth2RefreshToken token = new DefaultOAuth2RefreshToken(
					encode(encodedRefreshToken, authentication));
			if (refreshToken instanceof ExpiringOAuth2RefreshToken) {
				Date expiration = ((ExpiringOAuth2RefreshToken) refreshToken).getExpiration();
				encodedRefreshToken.setExpiration(expiration);
				token = new DefaultExpiringOAuth2RefreshToken(encode(encodedRefreshToken, authentication), expiration);
			}
			result.setRefreshToken(token);
		}
		return result;
	}

	protected String encode(OAuth2AccessToken accessToken, OAuth2Authentication authentication) {
		String content;
		try {
			content = objectMapper.formatMap(tokenConverter.convertAccessToken(accessToken, authentication));
		}
		catch (Exception e) {
			throw new IllegalStateException("Cannot convert access token to JSON", e);
		}
		String token = JwtHelper.encode(content, signer).getEncoded();
		return token;
	}
```

通过DefaultAccessTokenConverter的convertAccessToken将token的value转换为jwt格式的token。将USERNAME、AUTHORITIES、SCOPE、JTI、EXP、CLIENT_IDGRANT_TYPE、AUD(resourceId)放入Map中。

```java
//DefaultAccessTokenConverter的convertAccessToken方法
	public Map<String, ?> convertAccessToken(OAuth2AccessToken token, OAuth2Authentication authentication) {
		Map<String, Object> response = new HashMap<String, Object>();
		OAuth2Request clientToken = authentication.getOAuth2Request();

		if (!authentication.isClientOnly()) {
			response.putAll(userTokenConverter.convertUserAuthentication(authentication.getUserAuthentication()));
		} else {
			if (clientToken.getAuthorities()!=null && !clientToken.getAuthorities().isEmpty()) {
				response.put(UserAuthenticationConverter.AUTHORITIES,
							 AuthorityUtils.authorityListToSet(clientToken.getAuthorities()));
			}
		}

		if (token.getScope()!=null) {
			response.put(scopeAttribute, token.getScope());
		}
		if (token.getAdditionalInformation().containsKey(JTI)) {
			response.put(JTI, token.getAdditionalInformation().get(JTI));
		}

		if (token.getExpiration() != null) {
			response.put(EXP, token.getExpiration().getTime() / 1000);
		}
		
		if (includeGrantType && authentication.getOAuth2Request().getGrantType()!=null) {
			response.put(GRANT_TYPE, authentication.getOAuth2Request().getGrantType());
		}

		response.putAll(token.getAdditionalInformation());

		response.put(clientIdAttribute, clientToken.getClientId());
		if (clientToken.getResourceIds() != null && !clientToken.getResourceIds().isEmpty()) {
			response.put(AUD, clientToken.getResourceIds());
		}
		return response;
	}
```

通过JwtHelper的encode方法将content中的内容进行编码，先创建JwtHeader header = {"alg":"RS256","typ":"JWT"}，对header和content用"."进行组合，然后用base64加密，再使用秘钥进行签名。最后将header，content和crypto作为参数创建JwtImpl对象返回，在bytes()方法中分别将header，content和crypto通过base64编码后用"."进行连接。最终得到token的value值。refreshToken生成方式相同（会多一个ati，ati是accessToken的jti的值），只是程序中会先生成一个没有exp的refreshToken，然后从原refreshToken中获取过期时间后重新生成带有exp的refreshToken。

```java
public class JwtHelper {
	static byte[] PERIOD = utf8Encode(".");

	public static Jwt encode(CharSequence content, Signer signer) {
		return encode(content, signer, Collections.<String, String>emptyMap());
	}

	public static Jwt encode(CharSequence content, Signer signer,
			Map<String, String> headers) {
		JwtHeader header = JwtHeaderHelper.create(signer, headers);
		byte[] claims = utf8Encode(content);
		byte[] crypto = signer
				.sign(concat(b64UrlEncode(header.bytes()), PERIOD, b64UrlEncode(claims)));
		return new JwtImpl(header, claims, crypto);
	}

}

class JwtImpl implements Jwt {
	final JwtHeader header;

	private final byte[] content;

	private final byte[] crypto;

	private String claims;

	JwtImpl(JwtHeader header, byte[] content, byte[] crypto) {
		this.header = header;
		this.content = content;
		this.crypto = crypto;
		claims = utf8Decode(content);
	}

	@Override
	public byte[] bytes() {
		return concat(b64UrlEncode(header.bytes()), JwtHelper.PERIOD,
				b64UrlEncode(content), JwtHelper.PERIOD, b64UrlEncode(crypto));
	}

	@Override
	public String getEncoded() {
		return utf8Decode(bytes());
	}
}
```

**最终得到的token如下**

![21580557-90d99d11931bd2ad.png](https://upload-images.jianshu.io/upload_images/21580557-f00243dfa841b243.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


freshToken相比accessToken除了jti不同，相比多了"ati":"3463f614-d84d-431b-bc08-dac0c29d9417"，该ati就是accessToken的jti的值。

> **accessToken:**
> {"alg":"RS256","typ":"JWT"}{"aud":["res1"],"user_name":"1000","scope":["ROLE_ADMIN"],"exp":1600068422,"authorities":["hifun"],"jti":"a891bd48-5828-4572-bbc0-5c1f0c0449ba","client_id":"c1"}
> **refreshToken:**
> {"alg":"RS256","typ":"JWT"}{"aud":["res1"],"user_name":"1000","scope":["ROLE_ADMIN"],"ati":"a891bd48-5828-4572-bbc0-5c1f0c0449ba","exp":1600082822,"authorities":["hifun"],"jti":"341c06ce-5027-4304-961b-a97a9d1364ec","client_id":"c1"}

最最后在TokenEndpoint类中调用getResponse方法将OAuth2AccessToken 设置到返回参数中：

```java
//TokenEndpoint类的getResponse方法
	private ResponseEntity<OAuth2AccessToken> getResponse(OAuth2AccessToken accessToken) {
		HttpHeaders headers = new HttpHeaders();
		headers.set("Cache-Control", "no-store");
		headers.set("Pragma", "no-cache");
		headers.set("Content-Type", "application/json;charset=UTF-8");
		return new ResponseEntity<OAuth2AccessToken>(accessToken, headers, HttpStatus.OK);
	}
```



#### ③验证token流程

携带token访问资源，需要对token进行验证。

![21580557-63a59f0c9f8b78ff.png](https://upload-images.jianshu.io/upload_images/21580557-7da72961d9bd9704.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


流程概述：
1.从request中获取token，调用authenticate方法进行验证。
2.对token进行解析、**验证签名是否有效**、是否过期等信息，从token中获取用户和客户端信息。
3.通过从token中获取的信息创建OAuth2Request 和 已认证的UsernamePasswordAuthenticationToken，将这两个作为参数创建OAuth2Authentication。
4.**判断客户端是否有访问资源的权限**（判断OAuth2Authentication中的ResourceIds是否包含配置类中的ResourceId），然后将OAuth2Authentication设置为已认证（将authenticated属性设为true）。
5.将OAuth2Authentication设置到安全上下文中。完成校验，后续过滤器放行。
6.判断是否有权限

进入到OAuth2AuthenticationProcessingFilter过滤器的doFilter方法，从HttpServletRequest中获取Authorization或access_token(从请求头获取Authentication:Bearer xxxxxxxx--xxx，如果为null，则从请求参数获取access_token=xxxx-xxxx-xxxx)，拼接成PreAuthenticatedAuthenticationToken(Authentication子类)。包含了获取的accessToken的value，未经过认证。![21580557-9c6015dc6fc5ba74.png](https://upload-images.jianshu.io/upload_images/21580557-3e8fb151d88b603a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  将PreAuthenticatedAuthenticationToken强转为AbstractAuthenticationToken并设置Details。![21580557-203209e69b1b5779.png](https://upload-images.jianshu.io/upload_images/21580557-e7c8410219472364.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
   然后通过OAuth2AuthenticationManager的authenticate方法对该AbstractAuthenticationToken进行认证。代码如下。

```java
//OAuth2AuthenticationProcessingFilter的doFilter方法
	public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException,ServletException {

		final boolean debug = logger.isDebugEnabled();
		final HttpServletRequest request = (HttpServletRequest) req;
		final HttpServletResponse response = (HttpServletResponse) res;

		try {

			Authentication authentication = tokenExtractor.extract(request);
			
			if (authentication == null) {
				if (stateless && isAuthenticated()) {
					if (debug) {
						logger.debug("Clearing security context.");
					}
					SecurityContextHolder.clearContext();
				}
				if (debug) {
					logger.debug("No token in request, will continue chain.");
				}
			}
			else {
				request.setAttribute(OAuth2AuthenticationDetails.ACCESS_TOKEN_VALUE, authentication.getPrincipal());
				if (authentication instanceof AbstractAuthenticationToken) {
					AbstractAuthenticationToken needsDetails = (AbstractAuthenticationToken) authentication;
					needsDetails.setDetails(authenticationDetailsSource.buildDetails(request));
				}
				Authentication authResult = authenticationManager.authenticate(authentication);

				if (debug) {
					logger.debug("Authentication success: " + authResult);
				}

				eventPublisher.publishAuthenticationSuccess(authResult);
				SecurityContextHolder.getContext().setAuthentication(authResult);

			}
		}
		catch (OAuth2Exception failed) {
			SecurityContextHolder.clearContext();

			if (debug) {
				logger.debug("Authentication request failed: " + failed);
			}
			eventPublisher.publishAuthenticationFailure(new BadCredentialsException(failed.getMessage(), failed),
					new PreAuthenticatedAuthenticationToken("access-token", "N/A"));

			authenticationEntryPoint.commence(request, response,
					new InsufficientAuthenticationException(failed.getMessage(), failed));

			return;
		}

		chain.doFilter(request, response);
	}
```

BearerTokenExtractor的extract方法从参数中获取PreAuthenticatedAuthenticationToken。

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

与获取验证码或获取accessToken调用的autenticate方法不同，此处不是验证账号密码而是直接验证token是否有效。此处调用了OAuth2AuthenticationManager 类的authenticate方法进行验证。
对PreAuthenticatedAuthenticationToken中的token进行解码、签名验证，返回得到OAuth2Authentication，然后对设置的RESOURCE_ID进行判断，设置如下。

```java
    @Configuration
    @EnableResourceServer
    public class OrderServerConfig extends ResourceServerConfigurerAdapter {
        @Override
        public void configure(ResourceServerSecurityConfigurer resources) throws Exception {
            resources.resourceId(RESOURCE_ID)
                    .tokenStore(tokenStore)
                    .stateless(true);
        }

        @Override
        public void configure(HttpSecurity http) throws Exception {
            http.authorizeRequests()
//                    .antMatchers("/order/**").access("#oauth2.hasScope('ROLE_ADMIN')");
            .antMatchers("/order/**").permitAll();
        }
    }
```

进入OAuth2AuthenticationManager 类的authenticate方法。通过DefaultTokenServices 类的loadAuthentication方法获取OAuth2Authentication，如果OAuth2Authentication的resourceIds中不包含设置的RESOURCE_ID，验证失败抛出异常。最后将OAuth2Authentication的authenticated属性设为true表示已验证完成，并返回。

```java
public class OAuth2AuthenticationManager implements AuthenticationManager, InitializingBean {
	public Authentication authenticate(Authentication authentication) throws AuthenticationException {

		if (authentication == null) {
			throw new InvalidTokenException("Invalid token (token not found)");
		}
		String token = (String) authentication.getPrincipal();
		OAuth2Authentication auth = tokenServices.loadAuthentication(token);
		if (auth == null) {
			throw new InvalidTokenException("Invalid token: " + token);
		}

		Collection<String> resourceIds = auth.getOAuth2Request().getResourceIds();
		if (resourceId != null && resourceIds != null && !resourceIds.isEmpty() && !resourceIds.contains(resourceId)) {
			throw new OAuth2AccessDeniedException("Invalid token does not contain resource id (" + resourceId + ")");
		}

		checkClientDetails(auth);   //该方法在此场景下相当于空方法，直接跳过。

		if (authentication.getDetails() instanceof OAuth2AuthenticationDetails) {
			OAuth2AuthenticationDetails details = (OAuth2AuthenticationDetails) authentication.getDetails();
			// Guard against a cached copy of the same details
			if (!details.equals(auth.getDetails())) {
				// Preserve the authentication details from the one loaded by token services
				details.setDecodedDetails(auth.getDetails());
			}
		}
		auth.setDetails(authentication.getDetails());
		auth.setAuthenticated(true);
		return auth;

	}
	// ...
}
```

此处和前面生成OAuth2AccessToken使用的是相同的类，包括DefaultTokenServices ，JwtTokenStore，jwtTokenEnhancer和JwtHelper。`在如下DefaultTokenServices 类的loadAuthentication方法中，完成了对token的解析，签名验证，生成OAuth2Authentication 对象并判断是否过期。`然后通过readAuthentication方法通过OAuth2AccessToken对象获取OAuth2Authentication对象。因为没有在配置类中设置ClientDetailsService，所以不读取数据库直接返回OAuth2Authentication对象。

```java
public class DefaultTokenServices implements AuthorizationServerTokenServices, ResourceServerTokenServices,ConsumerTokenServices, InitializingBean {
	public OAuth2Authentication loadAuthentication(String accessTokenValue) throws AuthenticationException,
			InvalidTokenException {
		OAuth2AccessToken accessToken = tokenStore.readAccessToken(accessTokenValue);
		if (accessToken == null) {
			throw new InvalidTokenException("Invalid access token: " + accessTokenValue);
		}
		else if (accessToken.isExpired()) {
			tokenStore.removeAccessToken(accessToken);
			throw new InvalidTokenException("Access token expired: " + accessTokenValue);
		}

		OAuth2Authentication result = tokenStore.readAuthentication(accessToken);
		if (result == null) {
			// in case of race condition
			throw new InvalidTokenException("Invalid access token: " + accessTokenValue);
		}
		if (clientDetailsService != null) {   //未在配置类中设置clientDetailsService，不进入
			String clientId = result.getOAuth2Request().getClientId();
			try {
				clientDetailsService.loadClientByClientId(clientId);
			}
			catch (ClientRegistrationException e) {
				throw new InvalidTokenException("Client not valid: " + clientId, e);
			}
		}
		return result;
	}

	public OAuth2AccessToken extractAccessToken(String value, Map<String, ?> map) {
		DefaultOAuth2AccessToken token = new DefaultOAuth2AccessToken(value);
		Map<String, Object> info = new HashMap<String, Object>(map);
		info.remove(EXP);
		info.remove(AUD);
		info.remove(clientIdAttribute);
		info.remove(scopeAttribute);
		if (map.containsKey(EXP)) {
			token.setExpiration(new Date((Long) map.get(EXP) * 1000L));
		}
		if (map.containsKey(JTI)) {
			info.put(JTI, map.get(JTI));
		}
		token.setScope(extractScope(map));
		token.setAdditionalInformation(info);
		return token;
	}
	// ...
}
```

loadAuthentication方法中通过readAccessToken方法获取OAuth2AccessToken，在readAccessToken中又调用了DefaultTokenServices类的extractAccessToken方法。在该方法中将token解析出来值（）设置到新建的DefaultOAuth2AccessToken对象中，并返回。返回的DefaultOAuth2AccessToken值如下![21580557-2e45927164538279.png](https://upload-images.jianshu.io/upload_images/21580557-2531be169bed22bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
对DefaultOAuth2AccessToken进行校验，判断是否是refreshToken（如果包含ATI，则是refreshToken），如果不是则返回DefaultOAuth2AccessToken。

```java
public class JwtTokenStore implements TokenStore {
	@Override
	public OAuth2Authentication readAuthentication(OAuth2AccessToken token) {
		return readAuthentication(token.getValue());
	}

	@Override
	public OAuth2Authentication readAuthentication(String token) {
		return jwtTokenEnhancer.extractAuthentication(jwtTokenEnhancer.decode(token)); //调用了JwtAccessTokenConverter中的extractAuthentication方法
	}

	@Override
	public OAuth2AccessToken readAccessToken(String tokenValue) {
		OAuth2AccessToken accessToken = convertAccessToken(tokenValue);
		if (jwtTokenEnhancer.isRefreshToken(accessToken)) {
			throw new InvalidTokenException("Encoded token is a refresh token");
		}
		return accessToken;
	}

	private OAuth2AccessToken convertAccessToken(String tokenValue) {
		return jwtTokenEnhancer.extractAccessToken(tokenValue, jwtTokenEnhancer.decode(tokenValue));  //调用了JwtAccessTokenConverter中的extractAccessToken方法
	}
}
```

JwtAccessTokenConverter类在生成OAuth2AccessToken时调用enhance方法添加jti（将value作为jti）、更改了value和refreshToken。而在验证token时，该类的decode方法对token进行解码，验证签名，并返回一个Map包含了令牌中的客户端和用户信息。该Map用于后续生成OAuth2AccessToken和OAuth2Authentication 。

```java
public class JwtAccessTokenConverter implements TokenEnhancer, AccessTokenConverter, InitializingBean {
	protected Map<String, Object> decode(String token) {
		try {
			Jwt jwt = JwtHelper.decodeAndVerify(token, verifier);
			String claimsStr = jwt.getClaims();
			Map<String, Object> claims = objectMapper.parseMap(claimsStr);
			if (claims.containsKey(EXP) && claims.get(EXP) instanceof Integer) {
				Integer intValue = (Integer) claims.get(EXP);
				claims.put(EXP, new Long(intValue));
			}
			this.getJwtClaimsSetVerifier().verify(claims); //空方法，因为在decodeAndVerify已经完成签名校验
			return claims;
		}
		catch (Exception e) {
			throw new InvalidTokenException("Cannot convert access token to JSON", e);
		}
	}

	@Override
	public OAuth2Authentication extractAuthentication(Map<String, ?> map) {
		return tokenConverter.extractAuthentication(map);  //调用了DefaultAccessTokenConverter 类中的extractAuthentication方法
	}
	// ...
}
```

JwtHelper的decodeAndVerify方法对token进行解码并使用公钥验证签名是否有效，返回生成的Jwt对象。返回的Jwt对象和逻辑代码如下。![21580557-1317d4aa88d1ae36.png](https://upload-images.jianshu.io/upload_images/21580557-f5259fe4c461061e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```java
public class JwtHelper {
	public static Jwt decodeAndVerify(String token, SignatureVerifier verifier) {
		Jwt jwt = decode(token);
		jwt.verifySignature(verifier);

		return jwt;
	}

	public static Jwt decode(String token) {
		int firstPeriod = token.indexOf('.');
		int lastPeriod = token.lastIndexOf('.');

		if (firstPeriod <= 0 || lastPeriod <= firstPeriod) {
			throw new IllegalArgumentException("JWT must have 3 tokens");
		}
		CharBuffer buffer = CharBuffer.wrap(token, 0, firstPeriod);
		// TODO: Use a Reader which supports CharBuffer
		JwtHeader header = JwtHeaderHelper.create(buffer.toString());

		buffer.limit(lastPeriod).position(firstPeriod + 1);
		byte[] claims = b64UrlDecode(buffer);
		boolean emptyCrypto = lastPeriod == token.length() - 1;

		byte[] crypto;

		if (emptyCrypto) {
			if (!"none".equals(header.parameters.alg)) {
				throw new IllegalArgumentException(
						"Signed or encrypted token must have non-empty crypto segment");
			}
			crypto = new byte[0];
		}
		else {
			buffer.limit(token.length()).position(lastPeriod + 1);
			crypto = b64UrlDecode(buffer);
		}
		return new JwtImpl(header, claims, crypto);
	}
	// ...
}
```

------

DefaultAccessTokenConverter 类中的extractAuthentication方法将JwtAccessTokenConverter的decode方法返回的包含了令牌中的客户端和用户信息的Map作为参数  

![21580557-aea5cbdddf41f994.png](https://upload-images.jianshu.io/upload_images/21580557-a12eb0aefa5ac8b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  

调用extractAuthentication方法返回已经认证的UsernamePasswordAuthenticationToken对象，然后将该对象与Map中的用户信息作为参数构建OAuth2Authentication 对象并返回。![21580557-995c4ee3be6c47af.png](https://upload-images.jianshu.io/upload_images/21580557-a35c71138f77e7e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


```java
public class DefaultAccessTokenConverter implements AccessTokenConverter {
	public OAuth2Authentication extractAuthentication(Map<String, ?> map) {
		Map<String, String> parameters = new HashMap<String, String>();
		Set<String> scope = extractScope(map);
		Authentication user = userTokenConverter.extractAuthentication(map);
		String clientId = (String) map.get(clientIdAttribute);
		parameters.put(clientIdAttribute, clientId);
		if (includeGrantType && map.containsKey(GRANT_TYPE)) {
			parameters.put(GRANT_TYPE, (String) map.get(GRANT_TYPE));
		}
		Set<String> resourceIds = new LinkedHashSet<String>(map.containsKey(AUD) ? getAudience(map)
				: Collections.<String>emptySet());
		
		Collection<? extends GrantedAuthority> authorities = null;
		if (user==null && map.containsKey(AUTHORITIES)) {
			@SuppressWarnings("unchecked")
			String[] roles = ((Collection<String>)map.get(AUTHORITIES)).toArray(new String[0]);
			authorities = AuthorityUtils.createAuthorityList(roles);
		}
		OAuth2Request request = new OAuth2Request(parameters, clientId, authorities, true, scope, resourceIds, null, null,
				null);
		return new OAuth2Authentication(request, user);
	}
	// ...
}
```

在extractAuthentication方法中调用了DefaultUserAuthenticationConverter的extractAuthentication方法。在该方法中，因为我们没有写UserDetailsService的实现类，所以跳过去数据库校验的username的步骤。直接创建已经认证的UsernamePasswordAuthenticationToken对象并返回。

```java
public class DefaultUserAuthenticationConverter implements UserAuthenticationConverter {
	public Authentication extractAuthentication(Map<String, ?> map) {
		if (map.containsKey(USERNAME)) {
			Object principal = map.get(USERNAME);
			Collection<? extends GrantedAuthority> authorities = getAuthorities(map);
			if (userDetailsService != null) {
				UserDetails user = userDetailsService.loadUserByUsername((String) map.get(USERNAME));
				authorities = user.getAuthorities();
				principal = user;
			}
			return new UsernamePasswordAuthenticationToken(principal, "N/A", authorities);
		}
		return null;
	}
}
```


<br>

### 1.2.3 刷新token流程
待续......

