<template>
    <div class="small-card d-flex flex-column align-items-center">
        <div class="title">
            Neuen Test erstellen
        </div>

        <button class="primary create-btn" 
                type="button" 
                @click.stop="onClick"
                :disabled="!hasClickListener">
            <PlusIcon class="plus-icon" />
        </button>
    </div>
</template>

<script>
    import PlusIcon from '@/../public/assets/images/plus-icon.svg';

    export default {
        name: "CreateTestCard",

        components: {
            PlusIcon
        },

        computed: {
            hasClickListener() {
                return Boolean(this.$listeners.click);
;
            }
        },

        methods: {
            onClick() {
                if (!this.hasClickListener) return;
                this.$emit("click");
            }
        }
    };
</script>

<style scoped>
    .title {
        font-size: 22px;
        margin-bottom: 16px;
    }

    .create-btn {
        max-width: 100px;
    }

        .create-btn:disabled .plus-icon path {
            stroke: currentColor;
        }

    .plus-icon path {
        stroke-width: 3;
    }
</style>
