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
            <el-form-item label="" v-if="form.tags.length">
                <div class="text-left">
                    <span v-for="i in form.tags" :key="i"
                        class="inline-block px-2 py-[2px]  m-1 rounded-md bg-red-100 text-[12px] text-[#333]">{{ i
                        }}</span>
                </div>
            </el-form-item>
            <el-form-item label="标签">
                <Select v-model="form.tags" class="w-full" :placeholder="`标签`" :get-position="getPosition"></Select>
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.des" type="textarea" placeholder="描述" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer flex justify-end items-center">
                <el-button @click="onDialogCancel" class="mr-1 w-12">取消</el-button>
                <el-button @click="onDialogConfirm" class="w-12" type="primary">{{ isAdd ? '添加' : '确认' }}</el-button>
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
import { ref, watch } from 'vue';

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
const getPosition = async () => {
    res = await bookmarkApi.getTagList({ tag: '', username: userStore.username })
    return res.status == 200 ? res.data : []
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

</script>

<style lang="scss" scoped></style>