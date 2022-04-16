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
                    <button type="submit" class="contrast" @click="login()">登录</button>
                </form>
            </div>
        </article>
    </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../store/user';
const userStore = useUserStore();
// onMounted(() => {
//     const userStore = useUserStore();
//     console.log(userStore.getToken);
// });

const loginForm = ref({
    username: '',
    password: '',
    remember: true
});
const router = useRouter();
const login = function () {
    if (!this.loginForm.username) {
        document.getElementsByName('username').focus();
    } else {
        userStore.login({
            username: this.loginForm.username,
            password: this.loginForm.password,
            remember: this.loginForm.remember
        });
        console.log(userStore.getToken);
        router.push('/');
        // const res = await userStore.login({
        //     username: this.loginForm.username,
        //     password: this.loginForm.password,
        //     remember: this.loginForm.remember
        // });
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
