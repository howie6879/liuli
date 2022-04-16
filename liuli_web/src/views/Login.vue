<template>
    <main class="container">
        <article class="grid">
            <div class="login-cover"></div>
            <div>
                <hgroup>
                    <h1>Liuli</h1>
                    <h2>琉璃开净界，薜荔启禅关</h2>
                </hgroup>
                <form @submit.prevent="">
                    <input
                        v-model="loginForm.username"
                        type="text"
                        name="username"
                        placeholder="用户名"
                        required
                    />
                    <input
                        v-model="loginForm.password"
                        type="password"
                        name="password"
                        placeholder="密码"
                        required
                    />
                    <fieldset>
                        <label for="remember">
                            <input
                                v-model="loginForm.remember"
                                type="checkbox"
                                role="switch"
                                id="remember"
                                name="remember"
                            />
                            记住我
                        </label>
                    </fieldset>
                    <button
                        aria-busy="false"
                        type="submit"
                        class="contrast login-submit"
                        @click="login()"
                    >
                        登录
                    </button>
                </form>
            </div>
        </article>
    </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../store/user';

const router = useRouter();
const userStore = useUserStore();

const loginForm = ref({
    username: '',
    password: '',
    remember: true
});

const login = function () {
    if (!this.loginForm.username) {
        document.getElementsByName('username').focus();
    } else {
        document.querySelector('.login-submit').setAttribute('aria-busy', 'true');
        userStore
            .login({
                username: this.loginForm.username,
                password: this.loginForm.password,
                remember: this.loginForm.remember
            })
            .then((res) => {
                if (res) {
                    // 进行提示
                    router.push('/');
                } else {
                    // 有结果表示正常请求
                    document.querySelector('.login-submit').setAttribute('aria-busy', 'false');
                }
            });
    }
};
</script>

<style scoped>
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
    background-image: url('/src/assets/images/ll_login_img.jpg');
    background-position: center;
    background-size: cover;
}

@media (min-width: 992px) {
    article.grid div.login-cover {
        display: block;
    }
}
</style>
