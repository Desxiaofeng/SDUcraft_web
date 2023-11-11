import { createStore } from 'vuex';

export default createStore({
  state: {
    host: 'www.sducraft.top',
    url: 'https://www.sducraft.top/',
    noticeAPI:'https://www.sducraft.top/api/notice/',
    vteamAPI:'https://www.sducraft.top/api/vteam/',
    vgroupAPI:'https://www.sducraft.top/api/vgroup/',
    vmemberAPI:'https://www.sducraft.top/api/vmember/',
    proxyserverAPI:'https://www.sducraft.top/api/proxyserver/',
    serverAPI:'https://www.sducraft.top/api/server/',
    imagesetforserverAPI:'https://www.sducraft.top/api/imagesetforserver/',
    imagesetforproxyserverAPI:'https://www.sducraft.top/api/imagesetforproxyserver/',
    //注意下面这个比较特殊，末尾没有'/'
    otherdownloadAPI:'https://www.sducraft.top/otherdownload',
    historynodeAPI:'https://www.sducraft.top/api/historynode/',
    imagesetforhistorynodeAPI:'https://www.sducraft.top/api/imagesetforhistorynode/',
    downloadAPI:'https://www.sducraft.top/api/download/',
    filesetfowdownloadAPI:'https://www.sducraft.top/api/filesetfordownload/',
    introductionAPI:'https://www.sducraft.top/api/introduction/',
    documentAPI:'https://www.sducraft.top/api/document/',
    activityAPI:'https://www.sducraft.top/api/activity/',
    imagesetforactivityAPI:'https://www.sducraft.top/api/imagesetforactivity/'
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  },
});
