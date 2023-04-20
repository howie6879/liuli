<template>
    <div class="app-content flex flex-col bg-white">
        <div class="h-full flex justify-between ">
            <!-- 左侧书签 -->
            <div class="flex-grow">
                <!-- 搜索框 -->
                <el-input v-model="searchInput" class="searchInput max-w-[600px] min-w-[400px] w-full mb-4" size="large"
                    placeholder="Search" :prefix-icon="Search" @keyup.enter="onSearchBm()" />
                <!-- 书签列表 -->
                <div v-if="bmList.length" class="min-h-[calc(75vh)] flex flex-col justify-between">
                    <div>
                        <div v-for="i in bmList" :key="i.url" class="p-1">
                            <!-- 书签标题 -->
                            <a class="font-medium text-slate-500 text-lg cursor-pointer hover:text-black" :href="i.url"
                                target="_blank">{{
                                    i.title }}</a>
                            <!-- 书签的标签和描述 -->
                            <div>
                                <!-- 标签 -->
                                <span v-if="i.tags.length" class="mr-2 border-r-2 border-gray-300 text-sm">
                                    <span v-for="j in i.tags" class="mr-2 cursor-pointer text-[#e2989e] hover:underline"
                                        @click="onGetBookmarkFromTag(j)">#
                                        {{ j }}</span>
                                </span>
                                <!-- 描述 -->
                                <span class="text-sm text-[#409eff]">{{ i.des }}</span>
                            </div>
                            <!-- 书签操作 收藏时间 -->
                            <div class="text-xs text-gray-400">
                                <span class="pr-2 mr-2 border-r border-gray-400">{{ fromNow(i.updated_at!) }}</span>
                                <span>
                                    <span class="cursor-pointer hover:text-gray-600 mr-2" @click="onEditBM(i)">编辑</span>
                                    <el-popconfirm title="是否删除?" :teleported="false" @confirm="onDeleteBM(i.url)">
                                        <template #reference>
                                            <span class="cursor-pointer hover:text-gray-600">删除</span>
                                        </template>
                                    </el-popconfirm>
                                </span>
                            </div>
                        </div>
                    </div>
                    <!-- 分页 -->
                    <div class="mt-6 flex items-center justify-center">
                        <el-pagination v-model:current-page="page" :page-size="15" :page-sizes="[100, 200, 300, 400]"
                            layout="total, prev, pager, next, jumper" :total="total" @current-change="onCurrentChange" />
                    </div>
                </div>
                <div v-else class="text-sm">暂无书签</div>

            </div>
            <!-- 右侧标签 -->
            <div class="flex flex-col items-end w-1/4 flex-shrink-0 ml-6 text-sm leading-6">
                <!-- 操作 -->
                <el-dropdown trigger="click" class="mb-[70px]">
                    <div class="flex items-center text-base">更多</div>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item @click="onAddBookmark()">
                                <span>添加</span>
                            </el-dropdown-item>
                            <el-upload ref="uploadRef" accept=".html" class="mb-0" :before-upload="onUploadSuccess"
                                :show-file-list="false"
                                action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15">
                                <el-dropdown-item>
                                    <span>导入书签</span>
                                </el-dropdown-item>
                            </el-upload>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
                <el-scrollbar class="w-full">
                    <div v-for="i in tagList">
                        <div v-if="i.length" class="tagList mb-4 px-2 text-base">
                            <span v-for="tag in i" class="mr-4 cursor-pointer text-gray-500 hover:underline"
                                @click="onGetBookmarkFromTag(tag)">{{ tag }}</span>
                        </div>
                    </div>
                </el-scrollbar>
            </div>
        </div>
        <editBookmarkDialog v-model="isShowDialog" :is-add="isAdd" :bm="bm" @on-update="getBookmark(), getTagList()">
        </editBookmarkDialog>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import editBookmarkDialog from './editBookmarkDialog.vue';
import { pinyin } from 'pinyin-pro'
import { UserStore } from '@/store/user'
import { bookmarkApi } from '@/api';
import { IBookMark } from '@/api/shareInterface';
import { ElNotification, UploadProps } from 'element-plus';
import { fromNow } from "@/utils/day"
import { Search } from "@element-plus/icons-vue"


let res
const userStore = UserStore()

const searchInput = ref('')
const bmList = ref([] as IBookMark[])
// [
//     {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com',
//         tag: ['极客', '阿波罗']
//     },
//     {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com7',
//         tag: ['极客', '阿波罗']
//     }, {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com66',
//         tag: ['极客', '阿波罗']
//     },
//     {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com3',
//         tag: ['极客', '阿波罗']
//     }, {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com34',
//         tag: ['极客', '阿波罗']
//     },
//     {
//         title: '一站式信息聚合阅读分享平台 - Liuli.io',
//         des: '一站式信息聚合阅读分享平台 - Liuli.io',
//         url: 'www.baidu.com123',
//         tag: ['极客', '阿波罗']
//     }
// ]
const page = ref(1)
const total = ref(100)

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

const tags = ref(['#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元', '#())', '极客', '阿波罗', '嗷嗷嗷', 'ajax', '阿萨德', '啊阿斯顿', '啊呀呀呀', '电影', '二次元'])

const isShowDialog = ref(false)
const isAdd = ref(true)
const bm = ref({
    title: '一站式信息聚合阅读分享平台 - Liuli.io',
    des: '一站式信息聚合阅读分享平台 - Liuli.io',
    url: 'www.baidu.com',
    tags: ['极客', '阿波罗'],
    updated_at: 0,
})

const onEditBM = (bmData: IBookMark) => {
    (bm.value as IBookMark) = bmData
    isAdd.value = false
    isShowDialog.value = true
}

const onSearchBm = async () => {
    page.value = 1
    res = await bookmarkApi.searchBM({ page: page.value, page_size: 15, url: '', des: '', title: searchInput.value, tags: [] as string[], username: userStore.username })
    if (res.status == 200)
        bmList.value = res.data.rows, total.value = res.data.total
}

const onAddBookmark = () => {
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
            tags: [],
            des: '',
            title: '',
            url: '',
        }
        let errorBmTime = 0
        for (let i = 0; i <= bmDom.length; i++) {
            // console.log(bmDom.item(i)!.href)
            data.url = bmDom.item(i)!.href ? bmDom.item(i)!.href : ''
            data.title = bmDom.item(i)!.innerText ? bmDom.item(i)!.innerText : ''
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
    }
    return false;
}

const onDeleteBM = async (url: string) => {
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

const onGetBookmarkFromTag = async (tag: string) => {
    page.value = 1
    searchInput.value = ''
    res = await bookmarkApi.searchBM({ page: page.value, page_size: 15, url: '', des: '', title: '', tags: [tag] as string[], username: userStore.username })
    if (res.status == 200)
        bmList.value = res.data.rows, total.value = res.data.total
}

//分页器监听
const onCurrentChange = async () => {
    await getBookmark();
};

const getBookmark = async () => {
    // 获取bmList
    res = await bookmarkApi.searchBM({ page: page.value, page_size: 15, url: '', des: '', title: '', tags: [] as string[], username: userStore.username })
    if (res.status == 200)
        bmList.value = res.data.rows.reverse(), total.value = res.data.total
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
.tagList:first-child {
    &::first-letter {
        color: #409eff
    }
}

:deep(.searchInput.el-input .el-input__wrapper) {
    border-radius: 50px;

    .el-input__prefix {
        font-size: 20px;
        margin-left: 5px;
    }

    .el-input__inner {
        height: 60px;
        padding-left: 5px;
        font-size: 18px;
    }

}
</style>
