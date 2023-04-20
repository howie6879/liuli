<template>
  <div class="app-content bg-white">
    <div class="text-base">
      <div class="mb-3">
        <span class="inline-block w-[150px]">Token
          <el-tooltip class="box-item" effect="light" content="用于浏览器插件选项页面配置Token" placement="top">
            <el-icon :size="14">
              <InfoFilled />
            </el-icon>
          </el-tooltip>
        </span>
        <span>2f09a22a4c65dd7fe00ea3af4f290c1f</span>
      </div>
      <div class="mb-3">
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { bookmarkApi } from '@/api';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { onMounted, ref } from 'vue';

const userStore = UserStore()
let res
const uploadRef = ref()


const title = ref('配置管理');

onMounted(async () => {
  await userStore.initConfig()
})
</script>

<style scoped lang="scss"></style>
