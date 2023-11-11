import { createStore } from 'vuex';

export default createStore({
  state: {
    host: '192.168.22.132',
    url: 'http://192.168.22.132/',
    noticeAPI:'http://192.168.22.132/api/notice/',
    vteamAPI:'http://192.168.22.132/api/vteam/',
    vgroupAPI:'http://192.168.22.132/api/vgroup/',
    vmemberAPI:'http://192.168.22.132/api/vmember/',
    proxyserverAPI:'http://192.168.22.132/api/proxyserver/',
    serverAPI:'http://192.168.22.132/api/server/',
    imagesetforserverAPI:'http://192.168.22.132/api/imagesetforserver/',
    imagesetforproxyserverAPI:'http://192.168.22.132/api/imagesetforproxyserver/',
    //注意下面这个比较特殊，末尾没有'/'
    otherdownloadAPI:'http://192.168.22.132/otherdownload',
    historynodeAPI:'http://192.168.22.132/api/historynode/',
    downloadAPI:'http://192.168.22.132/api/download/',
    filesetfowdownloadAPI:'http://192.168.22.132/api/filesetfordownload/',
    introductionAPI:'http://192.168.22.132/api/introduction/',
    documentAPI:'http://192.168.22.132/api/document/',
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  },
});
