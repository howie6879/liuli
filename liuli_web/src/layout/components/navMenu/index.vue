<template>
    <div class="nav-menu">
        <div class="logo plr-20 flex f-ac-jc">
            <img class="img" :style="collapse ? 'height:40px' : 'height:50px'" src="~@/assets/images/logo.png"
                alt="logo" />
            <transition>
                <span v-show="!collapse" class="title ml-10">琉璃后台</span>
            </transition>
        </div>
        <el-menu :default-active="currentItemId" class="el-menu-vertical" background-color="#0c2135"
            :collapse="collapse" text-color="#b7bdc3" active-text-color="#0a60bd" @open="openMenu" collapse-transition>
            <template v-for="item in menuList" :key="item.name">
                <template v-if="!item.isHidden">
                    <menuItem :data="item" base-path="/">
                    </menuItem>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script setup>
import menuItem from './menuItem.vue'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { routes } from "@/router";

const props = defineProps({
    collapse: {
        type: Boolean,
        default: false
    }
})

const route = useRoute()
const router = useRouter()

// 筛选出一级菜单
const menuList = computed(() => {
    const list = routes.find(item => item.path === '/')
    return list.children ?? []
})

// 高亮的index
const currentItemId = computed(() => {
    const { path } = route
    return path
})

// 展开菜单时自动跳转
function openMenu(index, indexPath) {
    let path = indexPath[indexPath.length - 1]
    router.push(
        path
    )
}
</script>

<style scoped lang="scss">
.nav-menu {
    height: 100vh;
    background-color: #001529;

    .logo {

        height: 60px;


        .img {
            // height: 50px;
            margin: 0 10px;
        }

        .title {
            font-size: 16px;
            font-weight: 700;
            color: white;
        }
    }

    // 目录
    .el-submenu {
        background-color: #001529 !important;

        // 二级菜单 ( 默认背景 )
        .el-menu-item {
            padding-left: 50px !important;
            background-color: #0c2135 !important;
        }
    }

    :deep(.el-submenu__title) {
        background-color: #001529 !important;
    }

    // hover 高亮
    .el-menu-item:hover {
        color: #fff !important; // 菜单
    }

    .el-menu-item.is-active {
        color: #fff !important;
        background-color: #0a60bd !important;
    }
}
</style>
