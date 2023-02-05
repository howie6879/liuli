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
              <router-link :to="'/log'">个人设置</router-link>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon size="16px">
                <svg-icon name="svg-setting"></svg-icon>
              </el-icon>
              <router-link :to="'/log'">退出登陆</router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

  </div>
  <!-- <header>
    <div class="title">{{ title }}</div>
    <div class="dropdown">
      <div class="avatar" @click="showDropDown()">
        <ProfileAvatar username="liuli.io" :image="avatarConfig.imageUrl" :customSize="avatarConfig.customSize"
          :border="avatarConfig.border"></ProfileAvatar>
        <div id="dropdown-content">
          <a href="/setting"><img class="dropdown_ico" src="/src/assets/images/setting.svg" alt="logout" />
            &nbsp;个人设置</a>

          <div style="width: 100%; height: 0px; border-top: 1px solid rgba(0, 0, 0, 0.1); clear: both"></div>
          <a href="/login" @click="logout()">
            <img class="dropdown_ico" src="/src/assets/images/logout.svg" alt="logout" />
            &nbsp;退出登录</a>
        </div>
      </div>
    </div>
  </header> -->
</template>

<script setup>
import { ref } from "@vue/reactivity"

const emits = defineEmits(['foldChange'])
const props = defineProps({
  isCollapse: {
    type: String,
    default: '琉璃后台'
  }
})


function handleClick() {
  emits('foldChange')
}

const setting = ref(null)

function handleClickPic() {
  console.log('===setting.value===', setting.value.handleOpen)
  setting.value.handleOpen()
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
</style>

