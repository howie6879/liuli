<template>
  <div class="app-content flex flex-col bg-white max-h-[calc(100%-100px)]">
    <!-- searchBar -->
    <div class="flex gap-4 justify-between">
      <el-form inline :model="searchForm">
        <el-form-item label="文章标题:">
          <el-input v-model="searchForm.doc_name" placeholder="标题" clearable style="width: 250px"
            @keyup.enter="onSearch" />
        </el-form-item>
        <el-form-item label="文章类型:">
          <el-select clearable v-model="searchForm.doc_type" filterable placeholder="请选择文章类型" style="width: 250px">
            <el-option v-for="i in ['全部', ...doc_type_options]" :key="i" :label="i" :value="i === '全部' ? '' : i" />
          </el-select>
        </el-form-item>
        <el-form-item label="订阅源名称:">
          <el-select clearable v-model="searchForm.doc_source" filterable placeholder="请选择订阅源" style="width: 250px">
            <el-option v-for="i in ['全部', ...doc_source_options]" :key="i" :label="i" :value="i === '全部' ? '' : i" />
          </el-select>
        </el-form-item>
        <el-form-item label="订阅源目标:">
          <el-select clearable v-model="searchForm.doc_source_name" :disabled="!searchForm.doc_source" filterable
            placeholder="请选择订阅源目标" style="width: 250px">
            <el-option v-for="i in ['全部', ...doc_source_name_options]" :key="i"
              :label="searchForm.doc_source === '' ? '' : i" :value="i === '全部' ? '' : i" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="flex-none">
        <el-button type="primary" @click="onSearch" class="ml-[10px] mr-[12px]">搜索</el-button>
      </div>
    </div>

    <!-- table -->
    <el-table :data="list" stripe tooltip-effect="light" class="flex-grow">
      <el-table-column label="标题" min-width="300">
        <template #default="scope">
          <div class=" truncate">
            <a :href="scope.row.doc_link" target="_blank"
              class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.doc_name
              }}</a>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="地址" min-width="180">
        <template #default="scope">
          <div class="truncate">
            <el-icon :size="12" class="mr-2">
              <DocumentCopy @click="copyUrl(scope.row.doc_link)" class="cursor-pointer" />
            </el-icon>
            <a :href="scope.row.doc_link" target="_blank"
              class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.doc_link }}</a>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="文章类型" width="100" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc_type }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="订阅源目标" prop="des" width="200" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc_source_name }}
          </div>
        </template>
      </el-table-column>


      <el-table-column label="订阅源名称" width="180" :show-overflow-tooltip="true">
        <template #default="scope">
          <div class="truncate">
            {{ scope.row.doc_source }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="收集时间" width="250" prop="published_at">
        <template #default="scope">
          <span class="text-[13px]">
            {{ formatTimeStamp(scope.row.doc_ts, 'YYYY-MM-DD HH:mm:ss') }}
          </span>
        </template>
      </el-table-column>

      <el-table-column label="操作" fixed="right" width="105px">
        <template #default="scope">
          <el-tooltip class="box-item" effect="light" content="在线阅读">
            <el-button color="#409EFF" circle @click="onReader(scope.row.doc_id)">
              <template #icon>
                <el-icon color="#fff">
                  <View />
                </el-icon>
              </template>
            </el-button>
          </el-tooltip>

          <el-tooltip class="box-item" effect="light" content="收藏">
            <el-button color="#E6A23C" circle @click="onFavorite(scope.row.doc_id)">
              <template #icon>
                <el-icon color="#fff">
                  <Star />
                </el-icon>
              </template>
            </el-button>
          </el-tooltip>
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
import { onMounted, reactive, ref, watch } from 'vue';
import { UserStore } from '@/store/user';
import { formatTimeStamp } from "@/utils/day"
import { copyUrl } from "@/utils/tools"
import { articleApi, favoriteApi, statsApi } from '@/api';
import { ElNotification } from 'element-plus';
import { IArticle } from '@/api/shareInterface';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()

const userStore = UserStore();

const doc_source_options = ref([] as string[])
const doc_source_name_options = ref([] as string[])
const doc_type_options = ref(['book', 'wechat'])

let res
let doc_source_stats_dict: any

const searchForm = reactive({ doc_source: '', doc_source_name: '', doc_type: '', doc_name: '' })
const page = ref(1)
const total = ref(8)

const list = ref([] as IArticle[])

// 搜索
const onSearch = async () => {
  page.value = 1
  res = await getDescribeContent();
}

//分页器监听
const onCurrentChange = async () => {
  await getDescribeContent();
};

const onFavorite = async (_id: string) => {
  res = await favoriteApi.favoriteArticle({ username: userStore.username, doc_id: _id })
  if (res.status === 200) {
    ElNotification({
      message: '操作成功',
      type: 'success',
      duration: 2000
    });
    await getDescribeContent();
  } else {
    const msg = res.info ? res.info : '服务器超时';
    ElNotification({
      message: msg,
      type: 'error',
      duration: 2000
    });
  }
}

const onReader = (doc_id: string) => {
  window.open(`/reader?doc_id=${doc_id}`)
}

const getDescribeContent = async () => {
  // 获取订阅源内容
  res = await articleApi.searchArticle({ username: userStore.username, page: page.value, page_size: 15, ...searchForm })
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

watch(() => searchForm.doc_source, () => {
  searchForm.doc_source_name = ''
  if (searchForm.doc_source === '') return
  doc_source_name_options.value = doc_source_stats_dict[searchForm.doc_source].rows
})

onMounted(async () => {
  await getDescribeContent()
  res = await statsApi.getStats({ username: userStore.username })
  if (res.status == 200) {
    doc_source_stats_dict = res.data.doc_source_stats_dict
    doc_source_options.value = Object.keys(doc_source_stats_dict)
  } else {
    const msg = res.info ? res.info : '服务器超时';
    ElNotification({
      message: msg,
      type: 'error',
      duration: 2000
    });
  }
})

</script>

<style lang="scss" scoped>
:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>

