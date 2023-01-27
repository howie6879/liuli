<template>
  <div class="forkme">
    <a
      class="github-fork-ribbon fixed"
      href="https://github.com/liuli-io/liuli"
      target="_blank"
      data-ribbon="Fork me on GitHub"
      title="Fork me on GitHub"
    >
      Fork me on GitHub
    </a>
  </div>
  <main class="container">
    <article class="grid">
      <div class="login-cover"></div>
      <div>
        <hgroup>
          <h1>
            <a target="_blank" style="color: #e2989e" href="https://github.com/liuli-io/liuli"
              >Liuli</a
            >
          </h1>
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
            <!-- <label for="remember">
              <input
                v-model="loginForm.remember"
                type="checkbox"
                role="switch"
                id="remember"
                name="remember"
              />
              记住我
            </label> -->
          </fieldset>
          <button aria-busy="false" type="submit" class="login-submit" @click="login()">
            登录
          </button>
        </form>
      </div>
    </article>
  </main>
</template>

<script setup>
import { ref } from 'vue';

import { useRouter } from 'vue-router';
import { useUserStore } from '../store/user';
import { toaster } from '../utils/notification';

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
        if (res.status == 200) {
          // toaster.success('登陆成功');
          window.location.href = '/';
          // setTimeout("window.location.href = '/'", 500);
        } else {
          const msg = res.info ? res.info : '服务器超时';
          toaster.error(msg);
          document.querySelector('.login-submit').setAttribute('aria-busy', 'false');
        }
      });
  }
};
</script>

<style scoped>
@import '../../public/static/css/gh-fork-ribbon.min.css';

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

.login-submit {
  background: #e2989e;
  border: none;
}

.login-submit:hover {
  background: #e8878f;
  border: none;
}
</style>
