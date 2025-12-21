<template>
    <button class="switch"
            :disabled="disabled"
            :aria-pressed="value.toString()"
            :aria-label="title"
            @click="onToggle">
        <span class="knob" :class="{ on: value }"></span>
    </button>
</template>

<script>
    export default {
        props: {
            value: Boolean,
            title: String,
            disabled: Boolean
        },
        methods: {
            onToggle(event) {
                const newValue = !this.value;
                this.$emit('input', newValue);
                this.$emit('change', newValue, event);
            }
        }
    }
</script>

<style scoped>
    .switch {
        width: 44px;
        height: 22px;
        background: #ccc;
        border-radius: 20px;
        border: none;
        cursor: pointer;
        padding: 0;
        position: relative;
        transition: background-color 0.25s;
    }

    .knob {
        position: absolute;
        top: 2px;
        left: 2px;
        width: 18px;
        height: 18px;
        background: #fff;
        border-radius: 50%;
        transition: transform 0.25s;
    }

        .knob.on {
            transform: translateX(22px);
        }

    .switch[aria-pressed="true"] {
        background-color: var(--primary-color);
    }
</style>
