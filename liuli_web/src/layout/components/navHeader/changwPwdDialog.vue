<template>
    <el-dialog v-model="props.modelValue" title="修改密码" width="530px" :before-close="onClose">
        <el-form :model="form" label-width="55px">
            <el-form-item label="用户名">
                <span>{{ userStore.username }}</span>
            </el-form-item>
            <el-form-item label="旧密码">
                <el-input v-model="form.o_pwd" type="password" placeholder="旧密码" required />
            </el-form-item>
            <el-form-item label="新密码">
                <el-input v-model="form.n_pwd" type="password" placeholder="新密码" required />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer flex justify-end items-center">
                <el-button @click="onDialogCancel" class="mr-1">取消</el-button>
                <el-button @click="onDialogConfirm" type="primary">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { userApi } from '@/api';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { ref } from 'vue';

interface IProps {
    modelValue: boolean,
}
const props = defineProps<IProps>();
const emits = defineEmits(['update:modelValue']);

let res
const userStore = UserStore()

const form = ref({
    o_pwd: '',
    n_pwd: ''
})
const tagOptions = ref([] as string[])

//关闭dialog
const onClose = () => {
    emits('update:modelValue', false);
};
const onDialogCancel = () => {
    onClose()
}
const onDialogConfirm = async () => {
    if (!form.value.o_pwd.length || !form.value.n_pwd.length) return ElNotification({
        message: '请输入完整信息',
        type: 'warning',
        duration: 2000
    });
    res = await userApi.changePwd({ username: userStore.username, n_password: form.value.n_pwd, o_password: form.value.o_pwd })
    if (res.status == 200) {
        ElNotification({
            message: '修改成功',
            type: 'success',
            duration: 2000
        });
        emits('update:modelValue', false);
    } else {
        const msg = res.info ? res.info : '服务器超时';
        ElNotification({
            message: msg,
            type: 'error',
            duration: 2000
        });
    }

}


</script>

<style lang="scss" scoped></style>