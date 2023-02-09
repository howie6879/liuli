<template>
    <svg aria-hidden="true" class="svg-icon">
        <use :xlink:href="symbolId" />
    </svg>
</template>

<script>
import { defineComponent, computed } from 'vue'

export default defineComponent({
    name: 'SvgIcon',
    props: {
        prefix: {
            type: String,
            default: 'icon',
        },
        name: {
            type: String,
            required: true,
        },

    },
    setup(props) {
        const symbolId = computed(() => `#${props.prefix}-${props.name}`)
        return { symbolId }
    },
})
</script>
<style lang="scss" scoped>
.svg-icon {
    color: var(--el-menu-color);
}
</style>