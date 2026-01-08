<template>
    <div class="small-card">
        <div class="headline">{{ title }}</div>

        <div class="main">
            <div class="icon">
                <img v-if="iconSrc"
                     :src="iconSrc"
                     alt=""
                     class="icon-img" />
            </div>

            <div class="title">{{ value }}</div>
        </div>

        <div v-show="subtitle" class="subtitle" :class="subtitleClass">
            {{ subtitle }}
        </div>
    </div>
</template>

<script>
    export default {
        name: "StatsCard",

        props: {
            title: {
                type: String,
                required: true
            },
            value: {
                type: String,
                required: true
            },
            subtitle: {
                type: String,
                default: ""
            },
            subtitleClass: {
                type: String,
                default: ""
            },
            iconSrc: {
                type: String,
                required: true
            }
        }
    };
</script>

<style scoped>

    .headline {
        color: #6B6B6B;
        font-size: 16px;
        margin-bottom: 16px;
    }

    .main {
        display: flex;
        align-items: center;
        margin-bottom: 3px;
    }

    .icon {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
    }

    .icon-img {
        width: 34px;
        height: 34px;
    }

    .title {
        font-size: 28px;
    }

    .subtitle {
        font-size: 14px;
        color: #6B6B6B;
        min-height: 1rem;
    }

    .subtitle-positive {
        color: #2E8B57;
    }

    .subtitle-negative {
        color: #D90202;
    }
</style>
