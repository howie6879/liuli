<template>
  <div class="app-content flex flex-col bg-white max-h-[calc(100%-100px)]">
    <!-- table -->
    <el-table :data="list" stripe tooltip-effect="light" class="flex-grow">
      <el-table-column label="标题" min-width="300">
        <template #default="scope">
          <div class=" truncate">
            <a :href="scope.row.doc[0].doc_link" target="_blank"
              class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.doc[0].doc_name
              }}</a>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="地址" min-width="180">
        <template #default="scope">
          <div class="truncate">
            <el-icon :size="12" class="mr-2">
              <DocumentCopy @click="copyUrl(scope.row.doc[0].doc_link)" class="cursor-pointer" />
            </el-icon>
            <a :href="scope.row.doc[0].doc_link" target="_blank"
              class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.doc[0].doc_link }}</a>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="文章类型" width="100" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc[0].doc_type }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="订阅源目标" prop="des" width="200" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc[0].doc_source_name }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="订阅源名称" prop="des" width="180" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc[0].doc_source }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="更新时间" width="250" prop="published_at">
        <template #default="scope">
          <span class="text-[13px]">
            {{ formatTimeStamp(scope.row.updated_at, 'YYYY-MM-DD HH:mm:ss') }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="操作" fixed="right" width="105px">
        <template #default="scope">
          <el-tooltip class="box-item" effect="light" content="在线阅读">
            <el-button color="#409EFF" circle @click="">
              <template #icon>
                <el-icon color="#fff">
                  <View />
                </el-icon>
              </template>
            </el-button>
          </el-tooltip>

          <el-popconfirm title="是否删除?" @confirm="onDelete(scope.row.doc_id)" width="190px">
            <template #reference>
              <el-button color="#F45B65" circle>
                <el-icon color="#fff">
                  <Delete />
                </el-icon>
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination v-model:current-page="page" :page-size="15" :page-sizes="[100, 200, 300, 400]"
      class=" self-center mt-4" layout="total, prev, pager, next, jumper" :total="total"
      @current-change="onCurrentChange" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { UserStore, useUserStore } from '@/store/user';
import { formatTimeStamp } from "@/utils/day"
import { copyUrl } from "@/utils/tools"
import { favoriteApi, userApi } from '@/api';
import { ElNotification } from 'element-plus';
import { IArticle } from '@/api/shareInterface';

const userStore = UserStore();

let res

const page = ref(1)
const total = ref(1)

const list = ref([] as IArticle[])
//list 后端返回格式有问题

//分页器监听
const onCurrentChange = async () => {
  await getFavoriteContent();
};

const onDelete = async (_id: string) => {
  res = await favoriteApi.deleteFavoriteArticle({ username: userStore.username, doc_id_list: [_id] })
  if (res.status == 200) {
    ElNotification({
      message: '操作成功',
      duration: 2000,
      type: "success"
    })
    await getFavoriteContent()
  } else {
    const msg = res.info ? res.info : '服务器超时';
    ElNotification({
      message: msg,
      type: 'error',
      duration: 2000
    });
  }

}

const getFavoriteContent = async () => {
  // 获取收藏内容
  res = await favoriteApi.getFavorite({ username: userStore.username, page: page.value, page_size: 15 })
  if (res.status == 200) {
    console.log(res.data)
    list.value = res.data.rows
    total.value = res.data.total
  } else {
    const msg = res.info ? res.info : '服务器超时';
    ElNotification({
      message: msg,
      type: 'error',
      duration: 2000
    });
  }
}

onMounted(async () => {
  await getFavoriteContent()
});
</script>

<style lang="scss" scoped>
:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>

