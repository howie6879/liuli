import { ICommonResp } from '@/api/shareInterface';

export interface IGetStatsParams {
    username: string;
}

export interface IGetStatsResp extends ICommonResp {
    data:{
      doc_counts: number,
        doc_source_counts: number,
        doc_source_stats_dict: {
            liuli_book: {
                counts: number,
                doc_source_alias_name: string,
                rows: any[],
                rows_info: string[]
            },
            liuli_wechat_feeddd: {
                counts: number,
                doc_source_alias_name: string,
                rows: any[],
                rows_info: string[]
            },
            liuli_wechat_sg: {
                counts: number,
                doc_source_alias_name: string,
                rows: any[],
                rows_info: string[]
            }
        }
    }
}

