<template>
  <div class="app-content flex flex-col bg-white max-h-[calc(100%-100px)]s">
    <!-- table -->
    <el-table :data="logList" stripe tooltip-effect="light" class="flex-grow">
      <el-table-column label="标题" prop="doc_name" min-width="340">
      </el-table-column>

      <el-table-column label="订阅源" min-width="100">
        <template #default="scope">
          <div>
            {{ scope.row.type == 1 ? '备份' : '分发' }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="目标" width="350">
        <template #default="scope">
          <el-tooltip class="box-item" :disabled="!scope.row.target.length" effect="light" placement="top-start">
            <div class="w-auto overflow-hidden text-overflow-hidden cursor-pointer" v-if="scope.row.target.length">
              <el-tag v-for="i in scope.row.target" class="mr-1" :key="i">{{ i }}</el-tag>
            </div>
            <div v-else>-</div>
            <template #content>
              <div>
                <span v-for="(i, index) in scope.row.target" class="mr-1" :key="i">{{
                  `${i}${index === scope.row.target.length - 1 ? '' : ' '}`
                }}</span>
              </div>
            </template>
          </el-tooltip>
        </template>
      </el-table-column>


      <el-table-column label="订阅源" prop="doc_source" min-width="200">
      </el-table-column>

      <el-table-column label="订阅源目标" prop="doc_source_name" min-width="260">
      </el-table-column>

      <el-table-column label="操作时间" width="250" prop="published_at">
        <template #default="scope">
          <span class="text-[13px] cursor-pointer">
            {{ formatTimeStamp(scope.row.updated_at, 'YYYY-MM-DD HH:mm:ss') }}
          </span>
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
import { onMounted, ref } from 'vue';
import { formatTimeStamp } from "@/utils/day"

const logList = ref([
  {
    doc_name: '第五百四十章 新神没几个脑子是正常的',
    type: 1,
    target: ['gitHub', 'MongoDB'],
    doc_source: 'liuli_book',
    doc_source_name: '谁还不是个修行者了',
    updated_at: 1683258902,
  },
])
const page = ref(1)
const total = ref(6)

//分页器监听
const onCurrentChange = async () => {
  await getLog();
};

const getLog = async () => {

}

onMounted(async () => {
  await getLog()
});
</script>

<style></style>
