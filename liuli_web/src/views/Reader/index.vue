<template>
    <div class="w-full min-w-[680px] h-auto min-h-screen p-10 bg-slate-50">
        <div class="w-full min-w-[600px] max-w-[1000px] mx-auto p-10 shadow-xl bg-orange-50">
            <h3 class=" text-center text-3xl mb-6">{{ articleItem?.doc_name ? articleItem?.doc_name : '暂无文章' }}</h3>
            <div v-if="articleItem?.doc_core_html" v-html="articleItem?.doc_core_html" class="leading-[60px] text-xl"></div>
        </div>>
    </div>
</template>

<script lang="ts" setup>
import { articleApi } from '@/api';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()

let res

const articleItem = ref()

const userStore = UserStore()

onMounted(async () => {
    if (!route.query.doc_id) return
    res = await articleApi.getArticle({ username: userStore.username, doc_id: route.query.doc_id as string })
    if (res.status == 200) {
        articleItem.value = res.data
        document.title = articleItem.value.doc_name + ' - ' + document.title
        console.log(articleItem.value)

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

<style lang="scss" scoped></style>