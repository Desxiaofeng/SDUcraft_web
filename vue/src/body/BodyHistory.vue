<template>
    <div class="mainLayout"  :style="{boxShadow: `var(--el-box-shadow)`}">
    <el-timeline style="margin-right: 0; padding: 1em;">
      <el-timeline-item v-for="historynode in historynodes" :timestamp="historynode.date.slice(0,10)" placement="top" 
      :type="chooseType(historynode)" :hollow="this.historynodes[0]==historynode">
        <el-card>
          <p>{{ historynode.content }}</p>
          <template v-for="img in imagesetforhistorynode">
            <el-image v-if="img.historynode==historynode.id" :src="img.img" lazy />
            <figcaption v-if="img.historynode==historynode.id" style="text-align: center;">{{ img.name }}</figcaption>
          </template>
        </el-card>
      </el-timeline-item>
    </el-timeline>
    </div>
</template>
  

<script>
import axios from 'axios';

export default{
    data(){
        return{
            historynodes:null,
            imagesetforhistorynode:null,
        }
    },
    methods:{
        sortTimes(times) {
            return times.sort((a, b) => {
                const dateA = new Date(a.date);
                const dateB = new Date(b.date);
                return dateB - dateA;
            });
        },
        chooseType(historynode){
            if(this.historynodes[0]==historynode){
                return 'primary'
            }
            if(historynode.level==1){
                return 'danger'
            }
            return ''
        }
    },
    mounted(){
        axios.get(this.$store.state.historynodeAPI).then(response=>{
            this.historynodes=this.sortTimes(response.data)
        })
        axios.get(this.$store.state.imagesetforhistorynodeAPI).then(response=>{
            this.imagesetforhistorynode=response.data
        })
    },
}
</script>

<style scoped>
.mainLayout{
    margin: 0 18% ;
    min-height: 83vh;
    padding-top: 1em;
    background-color: #ffffff;

    border-left: 1px solid #cccccc;
    border-right: 1px solid #cccccc;
}

@media screen and (max-width: 800px) {
    .mainLayout{
        margin: 0;
        padding: 2em 0;
    }
}
</style>