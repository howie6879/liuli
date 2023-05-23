<template>
    <el-dialog v-model="props.modelValue" :title="props.isAdd ? '添加订阅源配置' : '编辑订阅源配置'" width="530px"
        :before-close="onClose">
        <el-button type="primary" link style=" float: right; margin-bottom: 10px;" @click="jsonFormat">格式化</el-button>
        <el-input v-model="doc" type="textarea" placeholder="描述" :rows="20" />
        <template #footer>
            <span class="dialog-footer flex justify-end items-center">
                <el-button @click="onDialogCancel" class="mr-1">取消</el-button>
                <el-button @click="onDialogConfirm" type="primary">{{ isAdd ? '添加' : '确认' }}</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { docSourceApi } from '@/api';
import { IDocSource } from '@/api/shareInterface';
import { UserStore } from '@/store/user';
import { ElNotification } from 'element-plus';
import { ref, watch } from 'vue';

interface IProps {
    modelValue: boolean,
    isAdd: boolean,
    doc_source?: IDocSource
}
const props = defineProps<IProps>();
const emits = defineEmits(['update:modelValue', 'onUpdate']);

let res

const doc = ref()

//关闭dialog
const onClose = () => {
    emits('update:modelValue', false);
};
const onDialogCancel = () => {
    onClose()
}
const onDialogConfirm = async () => {
    res = await docSourceApi.updateDocSource(JSON.parse(doc.value))
    if (res.status == 200)
        ElNotification({
            message: '操作成功',
            type: 'success',
            duration: 2000
        });
    emits('onUpdate');
    emits('update:modelValue', false);
}

const jsonFormat = () => {
    doc.value = JSON.stringify(JSON.parse(doc.value), null, '\t')
}

watch(props, async () => {
    if (!props.isAdd) {
        doc.value = JSON.stringify(props.doc_source, null, '\t')
    } else {
        doc.value = `{
    "name": "default",
    "username": "liuli",
    "author": "liuli_team",
    "doc_source_alias_name": "default",
    "doc_source": "default",
    "is_open": 1,
    "collector": {},
    "processor": {
        "before_collect": [],
        "after_collect": []
    },
    "sender": {
        "sender_list": ["wecom"],
        "query_days": 3,
        "delta_time": 3
    },
    "backup": {
        "backup_list": ["mongodb"],
        "query_days": 3,
        "delta_time": 3,
        "init_config": {},
        "after_get_content": []
    },
    "schedule": {
        "period_list": ["00:10", "12:10", "21:10"]
    }
}
        `
    }
})


</script>

<style lang="scss" scoped></style>