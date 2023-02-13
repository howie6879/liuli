<template>
  <header>
    <div class="title">{{ title }}</div>
    <div class="dropdown">
      <div class="avatar" @click="showDropDown()">
        <ProfileAvatar
          username="liuli.io"
          :image="avatarConfig.imageUrl"
          :customSize="avatarConfig.customSize"
          :border="avatarConfig.border"
        ></ProfileAvatar>
        <div id="dropdown-content">
          <!-- <a href="/"
            ><img class="dropdown_ico" src="/src/assets/images/logout.svg" alt="logout" /> Home</a
          > -->
          <a href="/setting"
            ><img class="dropdown_ico" src="/src/assets/images/setting.svg" alt="logout" />
            &nbsp;个人设置</a
          >

          <div
            style="width: 100%; height: 0px; border-top: 1px solid rgba(0, 0, 0, 0.1); clear: both"
          ></div>
          <a href="/login" @click="logout()">
            <img class="dropdown_ico" src="/src/assets/images/logout.svg" alt="logout" />
            &nbsp;退出登录</a
          >
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import ProfileAvatar from 'vue-profile-avatar';
import { toRefs, ref, onMounted, onBeforeUnmount } from 'vue';

import { useUserStore } from '../store/user';

const props = defineProps({
  //子组件接收父组件传递过来的值
  title: String
});

const { title } = toRefs(props);

const avatarConfig = ref({
  imageUrl: '/src/assets/images/logo.png',
  customSize: '40px',
  border: false
});

const userStore = useUserStore();
function logout() {
  userStore.logout().then((res) => {
    setTimeout("window.location.href = '/login'", 3000);
  });
}

function showDropDown() {
  var dropdown = document.getElementById('dropdown-content');
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

onMounted(() => {
  // 注册全局监听
  window.addEventListener('click', clickOther);
});

onBeforeUnmount(() => {
  // 解绑
  window.removeEventListener('click', clickOther);
});

// 全局监听函数
function clickOther(event) {
  if (!event.target.matches('.image')) {
    var dropdowns = document.getElementById('dropdown-content');
    if (dropdowns) {
      if (dropdowns.classList.contains('show')) {
        dropdowns.classList.remove('show');
      }
    }
  }
}
</script>

<style scoped>
header {
  height: 50px;
  border-left: 1px solid rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

header > div.title {
  float: left;
  width: 100px;
  color: #97a8be;
  cursor: text;
  font-size: 15px;
  line-height: 50px;
  margin-left: 10px;
}

header > div.dropdown {
  cursor: pointer;
  float: right;
  /* display: inline-block; */
  position: absolute !important;
  right: 10px !important;
  top: 5px !important;
  height: 50px;
}

#dropdown-content {
  display: none;
  position: absolute;
  background-color: #fff;
  width: 110px;
  font-size: 13px;
  overflow: auto;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  right: 0;
  z-index: 1;
}

#dropdown-content a {
  height: 40px;
  color: black;
  padding: 10px 18px;
  text-decoration: none;
  text-align: center;
  display: block;
  cursor: pointer;
}

#dropdown-content a:hover {
  background-color: #ededed85;
}

.show {
  display: block !important;
}

img.dropdown_ico {
  width: 15px;
  position: relative;
  margin-left: -5px;
  margin-top: -2px;
}
</style>
