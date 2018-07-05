<template>
    <div class="container">
        <div class="columns">
            <aside class="review column is-one-quarter">
                <form>
                    <div class="field">
                        <label class="label is-large">Your Score: </label>
                        <div class="control is-large">
                            <input class="input" type="number" :min="min" :max="max"/>
                        </div>
                    </div>
                </form>
            </aside>

            <div class="column is-three-quarters">
                <!-- random demographic information, can find a nice way to represent or table it -->
                <section class="basicinfo">
                    <h1 class="title">John Wick</h1>
                    <h2 class="subtitle">Baba Yaga</h2>
                </section>
                <!-- responses go here -->
                <section class="responses">
                
                </section>

                <!-- random web links can go here -->
                <section class="links">

                </section>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            answer: 0,
            min: 1,
            max: 10
        }
    },
    beforeRouteEnter(to, from, next) {
        next(() => {
        });
    }
}
</script>

<style scoped>
.basicinfo {

}
.responses {

}
.review {

}
</style>
