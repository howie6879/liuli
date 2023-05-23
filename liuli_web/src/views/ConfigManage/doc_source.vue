<template>
    <div class="app-content flex flex-col bg-white max-h-[calc(100%-100px)]">
        <!-- table -->
        <el-table :data="list" stripe tooltip-effect="light" class="flex-grow">

            <el-table-column label="订阅源名称" prop="doc_source" width="200">
            </el-table-column>

            <el-table-column label="依赖源名称" prop="doc_source_alias_name" width="150">
            </el-table-column>

            <el-table-column label="是否启动" width="150">
                <template #default="scope">
                    <span class="text-[13px]">
                        {{ scope.row.is_open ? '已启动' : '已关闭' }}
                    </span>
                </template>
            </el-table-column>

            <el-table-column label="备份器" width="300">
                <template #default="scope">
                    <el-tooltip class="box-item" :disabled="!scope.row.backup.backup_list.length" effect="light"
                        placement="top-start">
                        <div class="w-auto overflow-hidden text-overflow-hidden "
                            v-if="scope.row.backup.backup_list.length">
                            <el-tag v-for="i in scope.row.backup.backup_list" class="mr-1" :key="i">{{ i }}</el-tag>
                        </div>
                        <div v-else>-</div>
                        <template #content>
                            <div>
                                <span v-for="(i, index) in scope.row.backup.backup_list" class="mr-1" :key="i">{{
                                    `${i}${index === scope.row.backup.backup_list.length - 1 ? '' : ' '}`
                                }}</span>
                            </div>
                        </template>
                    </el-tooltip>
                </template>
            </el-table-column>

            <el-table-column label="分发器" min-width="300">
                <template #default="scope">
                    <el-tooltip class="box-item" :disabled="!scope.row.sender.sender_list.length" effect="light"
                        placement="top-start">
                        <div class="w-auto overflow-hidden text-overflow-hidden "
                            v-if="scope.row.sender.sender_list.length">
                            <el-tag v-for="i in scope.row.sender.sender_list" class="mr-1" :key="i">{{ i }}</el-tag>
                        </div>
                        <div v-else>-</div>
                        <template #content>
                            <div>
                                <span v-for="(i, index) in scope.row.sender.sender_list" class="mr-1" :key="i">{{
                                    `${i}${index === scope.row.sender.sender_list.length - 1 ? '' : ' '}`
                                }}</span>
                            </div>
                        </template>
                    </el-tooltip>
                </template>
            </el-table-column>


            <el-table-column label="更新时间" width="250" prop="published_at">
                <template #default="scope">
                    <span class="text-[13px] ">
                        {{ formatTimeStamp(scope.row.updated_at, 'YYYY-MM-DD HH:mm:ss') }}
                    </span>
                </template>
            </el-table-column>

            <el-table-column label="操作" fixed="right" width="105px">
                <template #header>
                    <div class="flex items-center">
                        <span class="mr-auto">操作</span>
                        <el-button type="primary" icon="Plus" circle @click="onAdd()" />
                    </div>
                </template>
                <template #default="scope">
                    <el-tooltip class="box-item" effect="light" content="编辑">
                        <el-button color="#409EFF" circle @click="onEdit(scope.row)">
                            <template #icon>
                                <el-icon color="#fff">
                                    <Edit />
                                </el-icon>
                            </template>
                        </el-button>
                    </el-tooltip>
                    <el-popconfirm title="是否删除?" @confirm="onDelete(scope.row.doc_source)" width="190px">
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
    </div>
    <docSourceDialog v-model="isShowDialog" :is-add="isAdd" :doc_source="doc_source" @on-update="getDocSource()">
    </docSourceDialog>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { docSourceApi } from '@/api';
import docSourceDialog from './docSourceDialog.vue';
import { IDocSource } from '@/api/shareInterface';
import { formatTimeStamp } from "@/utils/day"

const userStore = UserStore();

let res

const list = ref([] as IDocSource[])

const isShowDialog = ref(false)
const isAdd = ref(true)

const doc_source = ref()

const onAdd = () => {
    isAdd.value = true
    doc_source.value = ''
    isShowDialog.value = true
}

const onEdit = (source: IDocSource) => {
    isAdd.value = false
    doc_source.value = source
    isShowDialog.value = true
}

const onDelete = async (doc_source: string) => {
    res = await docSourceApi.deleteDocSource({ username: userStore.username, doc_source })
    if (res.status == 200) {
        ElNotification({
            message: '操作成功',
            duration: 2000,
            type: "success"
        })
        await getDocSource()
    } else {
        const msg = res.info ? res.info : '服务器超时';
        ElNotification({
            message: msg,
            type: 'error',
            duration: 2000
        });
    }
}

const getDocSource = async () => {
    res = await docSourceApi.getDocSource({ username: userStore.username, doc_source: '' })
    if (res.status == 200) {
        list.value = res.data
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
    await getDocSource()
});
</script>

<style lang="scss" scoped>
:deep(.el-form-item__label) {
    font-weight: 500;
}

:deep(.el-dialog .el-dialog__body) {
    padding-top: 0px !important;
}
</style>

