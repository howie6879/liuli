import dayjs from 'dayjs';

export const fromNow = (date:number)=>{
    return dayjs(date*1000).fromNow()
}

export const formatTimeStamp = (date: number, formatString = 'YYYY-MM-DD HH:mm:ss') => {
  try {
    return dayjs(date * 1000).format(formatString);
  } catch (error) {
    console.log('时间错误', error);
  }
};