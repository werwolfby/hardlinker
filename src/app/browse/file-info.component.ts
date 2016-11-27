import { Component, Input, OnInit } from "@angular/core";
import { FileInfo }                 from "./browse.service";

@Component({
    selector: 'file-info',
    template: `<span class="folder-path text-primary">{{file.folder}}/</span>` + 
        `<span>{{path}}</span>`,
})
export class FileInfoComponent {
    @Input()
    public file : FileInfo;

    public get path() : string {
        const items = [...(this.file.path || []), this.file.name];
        return items.join('/');
    }
}
