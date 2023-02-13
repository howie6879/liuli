<template>
  <div class="flex f-ac f-jsb header pl-10 pr-20">
    <div @click.stop="handleClick">
      <el-icon size="30px">
        <Expand v-if="isCollapse" />
        <Fold v-else />
      </el-icon>
    </div>
    <div>
      <el-dropdown ref="setting">
        <div class="avatar flex f-ac">
          <el-avatar :src="'/src/assets/images/logo.png'"></el-avatar>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <el-icon size="16px">
                <svg-icon name="svg-setting"></svg-icon>
              </el-icon>
              <router-link to="/log">
                <span class="drop-menu"> 个人设置 </span>
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon size="16px">
                <!-- <svg-icon name="svg-setting"></svg-icon> -->
                <SwitchButton />
              </el-icon>
              <router-link to="/login">
                <span class="drop-menu" @click="logout"> 退出登陆 </span>
              </router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref } from '@vue/reactivity';
import { useUserStore } from '@/store/user';

const emits = defineEmits(['foldChange']);
const props = defineProps({
  isCollapse: {
    type: Boolean,
    default: false
  }
});

function handleClick() {
  emits('foldChange');
}

const setting = ref(null);

function handleClickPic() {
  setting.value.handleOpen();
}

const userStore = useUserStore();
function logout() {
  userStore.logout().then((res) => {
    window.location.href = '/login';
  });
}
</script>

<style scoped lang="scss">
.header {
  height: 60px;

  .avatar {
    background-color: transparent;
    border: none;
    height: 60px;
    padding: 0;

    --box-shadow: none;

    &:hover {
      background-color: transparent;
      border: none;
      color: transparent;
    }
  }
}

.drop-menu {
  color: #000;
}
</style>
