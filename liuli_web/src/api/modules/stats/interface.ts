import { ICommonResp } from '@/api/shareInterface';

export interface IGetStatsParams {
    username: string;
}

export interface IGetStatsResp extends ICommonResp {
    data:{
      doc_counts: number,
        doc_source_counts: number,
        doc_source_stats_dict: {
            // 以下结构固定 对象名不确定
            any: {
                counts: number,
                doc_source_alias_name: string,
                rows: any[],
                rows_info: string[]
            },
        }
    }
}

