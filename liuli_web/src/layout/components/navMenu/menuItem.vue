<template>
    <div v-if="!data.isHidden">
        <!-- 不显示 -->
        <template v-if="data.children && data.children.length">
            <el-sub-menu :index="resolvePath(data.path, basePath)">
                <template #title>
                    <item v-if="data.meta" v-bind="data.meta">
                    </item>
                </template>
                <template v-for="subitem in data.children" :key="subitem.name">
                    <menuItem :data="subitem" :base-path="resolvePath(data.path, basePath)">
                    </menuItem>
                </template>
            </el-sub-menu>
        </template>
        <template v-else>
            <app-link :to="resolvePath(data.path, basePath)">
                <el-menu-item :index="resolvePath(data.path, basePath)">
                    <item v-bind="data.meta"></item>
                </el-menu-item>
            </app-link>
        </template>
    </div>
</template>

<script setup>
import appLink from '../appLink';
import item from './item'
import { resolvePath } from '@/utils'

const props = defineProps({
    data: {
        type: Object,
        default: () => ({})
    },
    basePath: {
        type: String,
        default: '/'
    }
})

function handleClick(path, te) {
    console.log('===path=234343==', path, te, arguments)

}

</script>
<style scoped lang="scss">
.menuitem {
    padding: 0 30px;

}

.router-link-active .router-link-exact-active {
    :v-deep(.svg-icon) {
        color: var(--el-menu-active-color)
    }
}
</style>