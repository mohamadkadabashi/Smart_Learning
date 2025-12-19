<template>
    <div class="tab-box">
        <div class="tab-header">
            <button v-for="(tab, index) in tabs"
                    :key="index"
                    :class="['tab-btn', { active: activeTab === index }]"
                    @click="activeTab = index">
                {{ tab }}
            </button>
        </div>
        <div class="tab-content">
            <slot :name="`tab-${activeTab}`"></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'TabContainer',
        props: {
            tabs: {
                type: Array,
                required: true,
                validator: (value) => value.length > 0 && value.length <= 2
            }
        },
        data() {
            return {
                activeTab: 0
            };
        }
    };
</script>

<style scoped>
.tab-box {
    border: 3px solid var(--secondary-color);
    border-radius: 50px;
    width: 50vw;
    height: 80vh;
    overflow: hidden;
}

.tab-header {
    display: flex;
    height: 10%;
}

.tab-btn {
    flex: 1;
    padding: 10px;
    background-color: transparent;
    border: none;
    border-bottom: 3px solid var(--secondary-color);
    cursor: pointer;
    font-size: 1.5rem;
}

    .tab-btn.active {
        background: var(--secondary-color);
        font-weight: bold;
    }

    .tab-btn:not(.active):hover {
        background: #E8E8E8;
    }

    .tab-btn.active:hover {
        background: #949494;
    }

.tab-content {
    padding: 20px;
    height: 70vh
}
</style>