<template>
    <main class="container">
        <article class="grid">
            <div class="login-cover"></div>
            <div>
                <hgroup>
                    <h1>Liuli</h1>
                    <h2>琉璃开净界，薜荔启禅关</h2>
                </hgroup>
                <form>
                    <input
                        type="text"
                        name="login"
                        placeholder="用户名"
                        aria-label="Login"
                        autocomplete="nickname"
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="密码"
                        aria-label="Password"
                        autocomplete="current-password"
                        required
                    />
                    <fieldset>
                        <label for="remember">
                            <input type="checkbox" role="switch" id="remember" name="remember" />
                            记住我
                        </label>
                    </fieldset>
                    <button type="submit" class="contrast" onclick="event.preventDefault()">
                        登录
                    </button>
                </form>
            </div>
        </article>
    </main>
</template>

<script>
export default {};
</script>

<style>
main.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: calc(100vh);
    padding: 1rem 0;
}

article {
    padding: 0;
    overflow: hidden;
}

article div {
    padding: 1rem;
}

article.grid div.login-cover {
    display: none;
    background-color: #374956;
    background-image: url('https://cdn.jsdelivr.net/gh/howie6879/oss/uPic/ll_login_demo.jpg');
    background-position: center;
    background-size: cover;
}

@media (min-width: 992px) {
    article.grid div.login-cover {
        display: block;
    }
}
</style>
