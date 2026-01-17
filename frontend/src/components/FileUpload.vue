<template>
    <div class="form-group">
        <label>Skript hochladen</label>
        <input type="file"
               id="file-upload"
               class="upload"
               @change="showFileName"
               title="Skript hochladen"
               multiple>
        <label for="file-upload" class="upload-btn"></label>

        <button type="button"
                v-if="files.length"
                class="files-header"
                @click="toggleFiles"
                :aria-expanded="showFiles"
                aria-controls="files-content">
            <span class="d-flex gap-1"><FolderIcon /> {{ files.length }} Datei(en) hochgeladen</span>
            <ArrowUpIcon v-if="showFiles" />
            <ArrowDownIcon v-if="!showFiles" />
        </button>
        <div v-if="showFiles && files.length" class="files-body" id="files-content">
            <div v-for="(file, i) in files"
                 :key="file.name + i"
                 class="file-row">
                <span class="file-name">{{ file.name }}</span>
                <button @click.stop="removeFile(i)"
                        class="delete-btn"
                        :aria-label="`Entferne die Datei ${file.name} aus der Liste der hochgeladenen Skripte`">
                    <DeleteIcon />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import DeleteIcon from '@/../public/assets/images/delete.svg';
    import ArrowUpIcon from '@/../public/assets/images/arrow-up-icon.svg';
    import ArrowDownIcon from '@/../public/assets/images/arrow-down-icon.svg';
    import FolderIcon from '@/../public/assets/images/folder-sharp.svg';

    export default {
        name: 'FileUpload',

        components: {
            DeleteIcon,
            ArrowUpIcon,
            ArrowDownIcon,
            FolderIcon
        },

        data() {
            return {
                files: [],
                showFiles: false
            }
        },

        emits: ['update-files'],

        methods: {
            showFileName(event) {
                const selectedFiles = Array.from(event.target.files);
                this.files.push(...selectedFiles);
                this.$emit('update-files', this.files);
            },

            removeFile(index) {
                this.files.splice(index, 1)
                this.$emit('update-files', this.files);

                if (this.files.length === 0) {
                    const input = document.getElementById('file-upload');
                    if (input) input.value = '';
                }
            },

            toggleFiles() {
                this.showFiles = !this.showFiles;
            }
        }
    }
</script>

<style scoped>
    .files-header {
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 12px;
        border: none;
        background-color: transparent;
    }

    .files-body {
        margin: 8px 16px 0;
        max-height: 160px;
        overflow-y: auto;
        padding-right: 4px;
    }

    .file-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
    }

    .file-name {
        max-width: 70%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .delete-btn {
        border: none;
        background-color: transparent;
    }

        .delete-btn svg {
            width: 20px;
            height: 20px;
            transition: transform 0.2s ease;
        }

        .delete-btn:hover svg {
            transform: scale(1.1);
        }
</style>