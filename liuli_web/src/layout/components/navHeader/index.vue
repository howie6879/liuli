<template>
  <div class="flex items-center justify-between header pl-[20px] pr-5">
    <div @click.stop="handleClick" class="cursor-pointer">
      <div class="w-[22px] h-[22px] rounded-[4px] bg-[rgb(225,225,225)] relative" v-if="!props.isCollapse">
        <div
          class="absolute w-[7px] h-[7px] border-[2px] border-black border-solid top-[8px] left-[6px] border-t-0 border-l-0 rounded-[1px]"
          style="transform: rotate(135deg)"></div>
        <div
          class="absolute w-[7px] h-[7px] border-[2px] border-[#00000052] border-solid top-[8px] left-[12px] border-t-0 border-l-0 rounded-[1px]"
          style="transform: rotate(135deg)"></div>
      </div>
      <div class="w-[22px] h-[22px] rounded-[4px] bg-[rgb(225,225,225)] relative" v-else>
        <div
          class="absolute w-[7px] h-[7px] border-[2px] border-black border-solid top-[8px] right-[6px] border-t-0 border-l-0 rounded-[1px]"
          style="transform: rotate(-45deg)"></div>
        <div
          class="absolute w-[7px] h-[7px] border-[2px] border-[#00000052] border-solid top-[8px] right-[12px] border-t-0 border-l-0 rounded-[1px]"
          style="transform: rotate(-45deg)"></div>
      </div>
    </div>
    <div>
      <el-dropdown ref="setting">
        <div class="avatar flex items-center">
          <el-avatar :src="'/src/assets/images/logo.png'"></el-avatar>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <el-icon size="16px">
                <svg-icon name="svg-setting" prefix="icon"></svg-icon>
              </el-icon>
              <router-link to="/log">
                <span class="drop-menu"> 设置 </span>
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon size="16px">
                <InfoFilled />
              </el-icon>
              <router-link to="/log">
                <span class="drop-menu"> 关于 </span>
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon size="16px">
                <!-- <svg-icon name="svg-setting"></svg-icon> -->
                <SwitchButton />
              </el-icon>
              <router-link to="/login">
                <span class="drop-menu" @click="logout"> 退出 </span>
              </router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from '@vue/reactivity';
import { UserStore } from '@/store/user';

const emits = defineEmits(['foldChange']);
const props = defineProps({
  isCollapse: {
    type: Boolean,
    default: false
  }
});
const userStore = UserStore();

function handleClick() {
  emits('foldChange');
}

const setting = ref();

function handleClickPic() {
  setting.value.handleOpen();
}

function logout() {
  userStore.logout()
}
</script>

<style scoped lang="scss">
.header {
  height: 60px;
  background: white;

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
