<template>
    <div ref="selectDivRef" v-click class="relative w-full text-gray-700 overflow-visible">
        <el-input v-model="searchText" type="text" :placeholder="props.placeholder" @focus="isShowPositionBox = true"
            @keydown.tab.space.enter="onKeyDownSelect()" />
        <div v-if="isShowPositionBox"
            class="absolute w-[calc(95%)] max-h-32  mt-2  z-30 left-2 overflow-y-scroll rounded-md border-1 bg-scroll bg-gray-100 scroll-box">
            <div v-for="i in currentPosition" :key="i" class="p-1 mx-2 text-left cursor-pointer hover:text-red-200"
                :class="activePosition.includes(i) ? 'text-red-300' : ''" @click="onSelect(i)">
                {{ i }}
            </div>
            <div v-if="!currentPosition.length" class="p-2 mx-2 text-left ">
                暂无
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { bookmarkApi } from '@/api';
import { UserStore } from '@/store/user';
import { onClickOutside } from '@vueuse/core'
import { onMounted, reactive, ref, watch } from 'vue';
interface IProps {
    modelValue: string[]
    placeholder?: string
}
const props = defineProps<IProps>()
const emits = defineEmits(['update:modelValue'])

const userStore = UserStore()

const selectDivRef = ref(null)

const searchText = ref('')

const isShowPositionBox = ref(false)

const originPosition = ref([] as string[])

const currentPosition = ref([] as string[])

let activePosition = reactive(props.modelValue as string[])

const onSelect = (selectItem: string) => {
    activePosition.includes(selectItem) ? activePosition.splice(activePosition.indexOf(selectItem), 1) : activePosition.push(selectItem)
    emits('update:modelValue', activePosition)
}

const onKeyDownSelect = () => {
    if (!searchText.value.trim()) return
    if (activePosition.includes(searchText.value.trim())) { activePosition.splice(activePosition.indexOf(searchText.value.trim()), 1) }
    else {
        activePosition.push(searchText.value.trim())
        originPosition.value.push(searchText.value.trim())
    }
    searchText.value = ''
}

onClickOutside(selectDivRef, () => {
    if (isShowPositionBox.value)
        isShowPositionBox.value = false
})

watch(searchText, () => {
    if (searchText.value.trim()) currentPosition.value = originPosition.value.filter(i => i.includes(searchText.value.trim()))
    else
        currentPosition.value = originPosition.value
}, { immediate: true })

watch(() => props.modelValue, () => {
    activePosition = props.modelValue
})

onMounted(async () => {
    let res = await bookmarkApi.getTagList({ tag: '', username: userStore.username })
    originPosition.value = res.status == 200 ? res.data.map(i => i.tag) : []
    currentPosition.value = originPosition.value;
})
</script>

<style lang="scss" scoped>
input {
    width: 100%;
    height: 34px;
    padding: 5px;
    margin: 0;
}
</style>
