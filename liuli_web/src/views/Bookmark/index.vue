<template>
    <div class="app-content flex flex-col bg-white max-h-[calc(100%-100px)]">
        <!-- searchBar -->
        <div class="flex gap-4 justify-between">
            <el-form inline :model="searchForm">
                <el-form-item label="标题:">
                    <el-input v-model="searchForm.title" placeholder="标题" clearable style="width: 250px"
                        @keyup.enter="onSearch" />
                </el-form-item>
                <el-form-item label="链接:">
                    <el-input v-model="searchForm.url" placeholder="链接" clearable style="width: 250px"
                        @keyup.enter="onSearch" />
                </el-form-item>
                <el-form-item label="标签:">
                    <el-select clearable v-model="searchForm.tags" filterable collapse-tags-tooltip collapse-tags multiple
                        placeholder="请输入文章标签" style="width: 250px">
                        <el-option v-for="i in tags" :key="i" :label="i" :value="i" />
                    </el-select>
                </el-form-item>
            </el-form>
            <div class="flex-none">
                <el-button type="primary" @click="onSearch" class="ml-[10px] mr-[12px]">搜索</el-button>
                <el-dropdown trigger="click">
                    <el-button color="#eee" circle icon="setting"></el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <!-- <el-dropdown-item @click="onAdd()">
                                <span>添加</span>
                            </el-dropdown-item> -->
                            <el-upload ref="uploadRef" accept=".html" class="mb-0" :before-upload="onUploadSuccess"
                                :show-file-list="false"
                                action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15">
                                <el-dropdown-item>
                                    <span>导入</span>
                                </el-dropdown-item>
                            </el-upload>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
        <!-- table -->
        <el-table :data="bmList" stripe tooltip-effect="light" class="flex-grow">
            <el-table-column label="标题" min-width="240">
                <template #default="scope">
                    <div class=" truncate">
                        <a :href="scope.row.url" target="_blank"
                            class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.title }}</a>
                    </div>
                </template>
            </el-table-column>

            <el-table-column label="链接" min-width="240">
                <template #default="scope">
                    <div class="truncate">
                        <el-icon :size="12" class="mr-2">
                            <DocumentCopy @click="copyUrl(scope.row.url)" class="cursor-pointer" />
                        </el-icon>
                        <a :href="scope.row.url" target="_blank"
                            class="hover:text-blue-400 hover:underline-blue-300 hover:underline">{{ scope.row.url }}</a>
                    </div>
                </template>
            </el-table-column>

            <el-table-column label="描述" prop="des" width="300" :show-overflow-tooltip="true">
                <template #default="scope">
                    <div class="truncate">
                        {{ `${scope.row.des.length > 0 ? scope.row.des : '-'}` }}
                    </div>
                </template>
            </el-table-column>

            <el-table-column label="标签" width="350">
                <template #default="scope">
                    <el-tooltip class="box-item" :disabled="!scope.row.tags.length" effect="light" placement="top-start">
                        <div class="w-auto overflow-hidden text-overflow-hidden" v-if="scope.row.tags.length">
                            <el-tag v-for="i in scope.row.tags" class="mr-1" :key="i">{{ i }}</el-tag>
                        </div>
                        <div v-else>-</div>
                        <template #content>
                            <div>
                                <span v-for="(i, index) in scope.row.tags" class="mr-1" :key="i">{{
                                    `${i}${index === scope.row.tags.length - 1 ? '' : ' '}`
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

                    <el-popconfirm title="是否删除?" @confirm="onDelete(scope.row.url)" width="190px">
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
    <editBookmarkDialog v-model="isShowDialog" :is-add="isAdd" :bm="bm" @on-update="getBookmark(), getTagList()">
    </editBookmarkDialog>
</template>

<script lang="ts" setup>
import { bookmarkApi } from '@/api';
import { IBookMark } from '@/api/shareInterface';
import { UserStore } from '@/store/user';
import editBookmarkDialog from './editBookmarkDialog.vue';
import { ElNotification, UploadProps } from 'element-plus';
import { pinyin } from 'pinyin-pro';
import { onMounted, reactive, ref } from 'vue';
import { formatTimeStamp } from "@/utils/day"
import { copyUrl } from "@/utils/tools"


let res
const userStore = UserStore()

const searchForm = reactive({ title: '', url: '', tags: [] })
const page = ref(1)
const total = ref(100)

const bmList = ref([] as IBookMark[])
const tagList = ref(
    {
        a: [] as string[],
        b: [] as string[],
        c: [] as string[],
        d: [] as string[],
        e: [] as string[],
        f: [] as string[],
        g: [] as string[],
        h: [] as string[],
        i: [] as string[],
        j: [] as string[],
        k: [] as string[],
        l: [] as string[],
        m: [] as string[],
        n: [] as string[],
        o: [] as string[],
        p: [] as string[],
        q: [] as string[],
        r: [] as string[],
        s: [] as string[],
        t: [] as string[],
        u: [] as string[],
        v: [] as string[],
        w: [] as string[],
        x: [] as string[],
        y: [] as string[],
        z: [] as string[],
        其他: [] as string[],
    }
)
const tags = ref([] as string[])

const isShowDialog = ref(false)
const isAdd = ref(true)

const bm = ref({
    title: '一站式信息聚合阅读分享平台 - Liuli.io',
    des: '一站式信息聚合阅读分享平台 - Liuli.io',
    url: 'www.baidu.com',
    tags: ['极客', '阿波罗'],
    updated_at: 0,
})

const onSearch = async () => {
    page.value = 1
    await getBookmark()
}

const onAdd = () => {
    isAdd.value = true
    isShowDialog.value = true
}

const onUploadSuccess: UploadProps['beforeUpload'] = async (rawFile) => {
    var reader = new FileReader();
    reader.readAsText(rawFile);
    reader.onload = async () => {
        const parser = new DOMParser();
        const dom = parser.parseFromString(reader.result as string, "text/html");
        const bmDom = dom.getElementsByTagName('a')
        const data = {
            tags: ['HTML导入'],
            des: '',
            title: '',
            url: '',
        }
        let errorBmTime = 0
        for (let i = 0; i < bmDom.length; i++) {
            console.log(bmDom.item(i))
            data.url = bmDom.item(i)?.href ? bmDom.item(i)!.href : ''
            data.title = bmDom.item(i)?.innerText ? bmDom.item(i)!.innerText : ''
            if (data.url) {
                res = await bookmarkApi.updateBM({ ...data, username: userStore.username })
                if (res.status != 200)
                    errorBmTime++;
            } else {
                errorBmTime++;
            }
        }
        ElNotification({
            type: 'success',
            message: `操作成功${errorBmTime !== 0 ? ` 有${errorBmTime}条书签导入失败` : ``}`,
            duration: 2000,
        });
        await getBookmark()
    }
    return false;
}

//分页器监听
const onCurrentChange = async () => {
    await getBookmark();
};

const onEdit = (bmData: IBookMark) => {
    (bm.value as IBookMark) = bmData
    isAdd.value = false
    isShowDialog.value = true
}

const onDelete = async (url: string) => {
    res = await bookmarkApi.deleteBM({ url_list: [url], username: userStore.username })
    if (res.status == 200) {
        ElNotification({
            message: '操作成功',
            duration: 2000,
            type: "success"
        })
        await getBookmark()
    }
}

const getBookmark = async () => {
    // 获取bmList
    res = await bookmarkApi.searchBM({ page: page.value, page_size: 15, url: searchForm.url, des: '', title: searchForm.title, tags: searchForm.tags, username: userStore.username })
    if (res.status == 200)
        bmList.value = res.data.rows, total.value = res.data.total
}

const getTagList = async () => {
    // 获取tagList
    res = await bookmarkApi.getTagList({ tag: '', username: userStore.username })
    if (res.status == 200) {
        tags.value = res.data.map(i => i.tag)
        tagList.value = {
            a: [] as string[],
            b: [] as string[],
            c: [] as string[],
            d: [] as string[],
            e: [] as string[],
            f: [] as string[],
            g: [] as string[],
            h: [] as string[],
            i: [] as string[],
            j: [] as string[],
            k: [] as string[],
            l: [] as string[],
            m: [] as string[],
            n: [] as string[],
            o: [] as string[],
            p: [] as string[],
            q: [] as string[],
            r: [] as string[],
            s: [] as string[],
            t: [] as string[],
            u: [] as string[],
            v: [] as string[],
            w: [] as string[],
            x: [] as string[],
            y: [] as string[],
            z: [] as string[],
            其他: [] as string[],
        }
        // 根据首字母分类tag
        tags.value.forEach(async i => {
            // 不是属于6字母的
            if (pinyin(i, { toneType: 'none' }).charCodeAt(0) > 123 || pinyin(i, { toneType: 'none' }).charCodeAt(0) < 97)
                Reflect.get(tagList.value, '其他').push(i)
            else
                Reflect.get(tagList.value, pinyin(i, { toneType: 'none' })[0]).push(i)
        })
    }
}

onMounted(async () => {
    await getBookmark()
    await getTagList()
});

</script>

<style lang="scss" scoped>
:deep(.el-form-item__label) {
    font-weight: 500;
}
</style>