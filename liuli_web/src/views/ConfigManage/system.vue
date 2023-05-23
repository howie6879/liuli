<template>
    <div class="flex flex-col">
        <div class=" self-end">
            <el-button v-if="!isEdit" color="#409EFF" circle @click="onEdit()">
                <template #icon>
                    <el-icon color="#fff">
                        <Edit />
                    </el-icon>
                </template>
            </el-button>
            <div v-else>
                <el-button color="#909399" circle @click="() => isEdit = false">
                    <template #icon>
                        <el-icon color="#fff">
                            <Close />
                        </el-icon>
                    </template>
                </el-button>
                <el-button color="#67C23A" circle @click="onConfirm()">
                    <template #icon>
                        <el-icon color="#fff">
                            <Finished />
                        </el-icon>
                    </template>
                </el-button>
            </div>
        </div>
        <el-descriptions direction="vertical" :column="2">
            <el-descriptions-item v-for="i in Object.keys(config)" :label="i">
                <span v-if="!isEdit">{{ config[i] == '' ? '暂未设置' : config[i] }}</span>
                <el-input v-else v-model="form[i]" style="width: 450px;" />
            </el-descriptions-item>
        </el-descriptions>
    </div>
</template>

<script lang="ts" setup>
import { configApi, userApi } from '@/api';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { onMounted, ref } from 'vue';

const userStore = UserStore();

let res

const isEdit = ref(false)

const config = ref({

})
const form = ref()

const onEdit = () => {
    isEdit.value = true
    form.value = JSON.parse(JSON.stringify(config.value))
}

const onConfirm = async () => {
    res = await configApi.updateConfig({ username: userStore.username, data: form.value })
    if (res.status == 200) {
        isEdit.value = false
        ElNotification({
            type: 'success',
            message: "操作成功",
            duration: 2000
        })
        await getConfig()
    } else {
        const msg = res.info ? res.info : '服务器超时';
        ElNotification({
            message: msg,
            type: 'error',
            duration: 2000
        });
    }

}

const getConfig = async () => {
    res = await configApi.getConfig({ username: userStore.username })
    if (res.status == 200) {
        config.value = res.data
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
    await getConfig()
});

// LL_JWT_SECRET_KEY: "5ff9920b0b055b9dabc3bba20b0c0104",
//     LL_X_TOKEN: "2f09a22a4c65dd7fe00ea3af4f290c1f",
//         LL_SPIDER_PHANTOMJS_KEY: "ak-65jwe-h7y7t-qt25g-9m0c5-etfg0",
//             LL_BARK_URL: "",
//                 LL_DD_TOKEN: "e5cc6947dcc9842d80bf1385aec525b229ac15fcad26e24a80ed3e6c267847c4",
//                     LL_DOMAIN: "",
//                         LL_GITHUB_DOMAIN: "",
//                             LL_GITHUB_REPO: "",
//                                 LL_GITHUB_TOKEN: "",
//                                     LL_TG_CHAT_ID: "",
//                                         LL_TG_TOKEN: "",
//                                             LL_WECOM_AGENT_ID: "1000004",
//                                                 LL_WECOM_ID: "wwee29721ad4f6e1c6",
//                                                     LL_WECOM_PARTY: "",
//                                                         LL_WECOM_SECRET: "F6Ncetsp_cM_xpLEKBvucR7GmlwiDyi8dGu7o0rykQs",
//                                                             LL_WECOM_TO_USER: ""
</script>

<style lang="scss" scoped></style>