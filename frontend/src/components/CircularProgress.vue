<template>
    <div class="progress-wrapper" :style="{ width: size + 'px', height: size + 'px' }">
        <svg class="progress-ring"
             :width="size"
             :height="size"
             :viewBox="`0 0 ${size} ${size}`">
            <circle class="progress-ring-bg"
                    :r="radius"
                    :cx="center"
                    :cy="center"
                    :stroke-width="stroke" />

            <circle class="progress-ring-circle"
                    :r="radius"
                    :cx="center"
                    :cy="center"
                    :stroke-width="stroke"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="dashOffset" />
        </svg>

        <div class="progress-text">
            <div class="percent">{{ value }}%</div>
            <div class="label">Tagesziel</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CircularProgress",
        props: {
            value: { type: Number, required: true },
            size: { type: Number, default: 160 },
            stroke: { type: Number, default: 13 }
        },
        data() {
            return {
                dashOffset: 0
            }
        },
        computed: {
            radius() {
                return (this.size - this.stroke) / 2;
            },
            center() {
                return this.size / 2;
            },
            circumference() {
                return 2 * Math.PI * this.radius;
            }
        },
        mounted() {
            this.dashOffset = this.circumference;

            setTimeout(() => {
                this.dashOffset = this.circumference * (1 - this.value / 100);
            }, 50);
        }
    }
</script>

<style scoped>
    .progress-wrapper {
        position: relative;
    }

    .progress-ring {
        transform: rotate(-90deg);
    }

    .progress-ring-bg {
        fill: #FAEFE7;
        stroke: #F0CFB9;
    }

    .progress-ring-circle {
        fill: none;
        stroke: #DD7A34;
        stroke-linecap: round;
        transition: stroke-dashoffset 1s ease;
    }

    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }

    .percent {
        font-size: 25px;
        font-weight: bold;
    }

    .label {
        font-size: 15px;
        color: #777;
    }
</style>
