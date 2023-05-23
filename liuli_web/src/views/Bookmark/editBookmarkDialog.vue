<template>
    <el-dialog v-model="props.modelValue" :title="props.isAdd ? '添加书签' : '编辑书签'" width="530px" :before-close="onClose">
        <el-form :model="form" label-width="40px">
            <el-form-item label="Url">
                <el-input v-if="isAdd" v-model="form.url" type="text" placeholder="Url" required />
                <a v-else :href="form.url" target="_blank" class="truncate">{{ form.url }}</a>
            </el-form-item>
            <el-form-item label="标题">
                <el-input v-model="form.title" type="text" placeholder="标题" required />
            </el-form-item>
            <el-form-item label="标签">
                <el-select v-model="form.tags" multiple filterable="true" allow-create clearable :reserve-keyword="false"
                    collapse-tags-tooltip collapse-tags :popper-append-to-body="false" placeholder="标签"
                    @keyup.enter="onElSelectEnter()" class="w-full">
                    <el-option v-for=" item in tagOptions " :key="item" :label="item" :value="item" />
                </el-select>

            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.des" type="textarea" placeholder="描述" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer flex justify-end items-center">
                <el-button @click="onDialogCancel" class="mr-1">取消</el-button>
                <el-button @click="onDialogConfirm" type="primary">{{ isAdd ? '添加' : '确认' }}</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { bookmarkApi } from '@/api';
import Select from '@/components/Select.vue';
import { UserStore } from '@/store/user';
import { checkUrl } from '@/utils/check';
import { ElNotification } from 'element-plus';
import { onMounted, ref, watch } from 'vue';

interface IProps {
    modelValue: boolean,
    isAdd: boolean,
    bm?: {
        title: string,
        url: string,
        des: string,
        tags: string[],
    }
}
const props = defineProps<IProps>();
const emits = defineEmits(['update:modelValue', 'onUpdate']);

let res
const userStore = UserStore()

const form = ref()
const tagOptions = ref([] as string[])

const onElSelectEnter = () => {
    // 选择的元素 null为没有选择
    const elSelectDropdownItemHover = document.querySelector('.el-select-dropdown__item .hover')
    // 第一个元素 为自己输入的
    const elSelectDropdownItemFirst = document.querySelector('.el-select-dropdown__item')
    // 第一个元素为null说明 自己没有输入 tagOptions也为空 直接返回
    if (elSelectDropdownItemFirst === null) return
    // 去除span标签
    const inputValue = elSelectDropdownItemFirst!.innerHTML.slice(6, -7)
    if (elSelectDropdownItemHover === null && !tagOptions.value.includes(inputValue)) {
        form.tags.value.push(inputValue)
        tagOptions.value.push(inputValue)
    }
}

//关闭dialog
const onClose = () => {
    emits('update:modelValue', false);
};
const onDialogCancel = () => {
    onClose()
}
const onDialogConfirm = async () => {
    if (!checkUrl(form.value.url)) return ElNotification({
        message: '请输入正确的Url',
        type: 'warning',
        duration: 2000
    });
    if (form.value.title.trim().length === 0) return ElNotification({
        message: '请输入标题',
        type: 'warning',
        duration: 2000
    });
    res = await bookmarkApi.updateBM({ ...form.value, username: userStore.username })
    if (res.status == 200)
        ElNotification({
            message: '操作成功',
            type: 'success',
            duration: 2000
        });
    emits('onUpdate');
    emits('update:modelValue', false);

}

watch(props, () => {
    if (props.isAdd)
        form.value = {
            title: '',
            url: '',
            des: '',
            tags: []
        }
    else form.value = JSON.parse(JSON.stringify(props.bm)), Reflect.deleteProperty(form.value, 'updated_at')
})

onMounted(async () => {
    res = await bookmarkApi.getTagList({ tag: '', username: userStore.username })
    tagOptions.value = res.status === 200 ? res.data.map((i: any) => i.tag) : []
})

</script>

<style lang="scss" scoped></style>