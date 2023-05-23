<template>
    <div class="app-content bg-white">
        <el-tabs v-model="activeName" type="card" @tab-click="onTabClick">
            <el-tab-pane v-for="metaData in tabPaneArray" :label="metaData.name" :name="metaData.name" :key="metaData.name">
                <component v-if="activeName === metaData.name" :is="metaData.component" class="p-2" />
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script lang="ts" setup>
import { UserStore } from '@/store/user';
import { defineAsyncComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()

const system = defineAsyncComponent(() => import('./system.vue'));
const doc_source = defineAsyncComponent(() => import('./doc_source.vue'));

const tabPaneArray = ref([{
    name: '系统配置',
    component: system
}, {
    name: '订阅源配置',
    component: doc_source
}])
const activeName = ref(route.query.activeName || '系统配置');

const onTabClick = (tab: any) => {
    activeName.value = tab.paneName
    router.push(
        {
            query: {
                ...route.query,
                activeName: tab.paneName
            }
        }
    )
}


</script>

<style scoped lang="scss"></style>


