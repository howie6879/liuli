<template>
  <div class="w-screen h-screen flex justify-center items-center">
    <div class="forkme">
      <a class="github-fork-ribbon fixed" href="https://github.com/liuli-io/liuli" target="_blank"
        data-ribbon="Fork me on GitHub" title="Fork me on GitHub">
        Fork me on GitHub
      </a>
    </div>
    <!-- <main class="container">
      <article class="grid">
        <div class="login-cover"></div>
        <div>
          <hgroup>
            <h1>
              <a target="_blank" style="color: #e2989e" href="https://github.com/liuli-io/liuli">Liuli</a>
            </h1>
            <h2>琉璃开净界，薜荔启禅关</h2>
          </hgroup>
          <form @submit.prevent="">
            <input v-model="loginForm.username" type="text" name="username" placeholder="用户名" required />
            <input v-model="loginForm.password" type="password" name="password" placeholder="密码" required />

            <button aria-busy="false" type="submit" class="login-submit" @click="login()">
              登录
            </button>
          </form>
        </div>
      </article>
    </main> -->

    <div class="flex justify-center items-center h-[450px] rounded-md overflow-hidden shadow-xl bg-white">
      <img src="/src/assets/images/ll_login_img.jpg" alt="" class="w-[550px] hidden h-full  xl:block">
      <div class="w-[550px] h-full p-4 pl-8">
        <a class="mb-1 text-[40px] font-bold text-[#e2989e]" href="https://github.com/howie6879/liuli"
          target="_blank">Liuli</a>
        <div class=" text-[20px]  text-[#73828c]">琉璃开净界，薜荔启禅关</div>
        <div class="my-10">
          <el-input v-model="loginForm.username" type="text" placeholder="用户名" class="username mb-6" required />
          <el-input v-model="loginForm.password" type="password" placeholder="密码" show-password required />
        </div>
        <button class="login-btn py-[15px] w-full text-center text-[20px] text-white bg-[#e2989e] rounded-md"
          @click="login()">登陆</button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import { useRouter } from 'vue-router';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';

const router = useRouter();
const userStore = UserStore();

const loginForm = ref({
  username: '',
  password: '',
});

const login = async function () {
  if (!loginForm.value.username) {
    document.querySelector('username')!.focus();
  } else {
    document.querySelector('.login-btn')!.setAttribute('aria-busy', 'true');
    const res = await userStore.login({ username: loginForm.value.username, password: loginForm.value.password })
    if (res.status == 200) {
      window.location.href = '/';
    } else {
      const msg = res.info ? res.info : '服务器超时';
      ElNotification({
        type: 'error',
        message: msg,
        duration: 2000,
      });
      document.querySelector('.login-btn')!.setAttribute('aria-busy', 'false');
    }
  }
}
</script>

<style scoped src="@/style/gh-fork-ribbon.min.css"></style>

<style scoped>
:deep(.el-input .el-input__inner) {
  height: 60px;
  padding: 15px 5px;
  font-size: 20px;
  color: #73828c;
}

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
