export interface FileInfo {
    folder: string;
    path: string[];
    name: string;
}

export interface LinkInfo extends FileInfo {
    links: FileInfo[];
}

export class FileInfoObject implements LinkInfo {
    public folder: string;
    public path:   string[];
    public name:   string;
    public links:  FileInfo[];
    public guess:  FileInfo;

    constructor(fileInfo: LinkInfo) {
        this.folder = fileInfo.folder;
        this.path = fileInfo.path || [];
        this.name = fileInfo.name;
        this.links = fileInfo.links || [];
    }

    get hasLinks() : boolean {
        return this.links.length > 0;
    }

    equals(fileInfo: FileInfo) : boolean {
        return this.folder == fileInfo.folder &&
               this.name == fileInfo.name &&
               FileInfoObject._equals(this.path, fileInfo.path || []);
    }

    prepareLink() : LinkInfo {
        if (!this.guess) {
            throw "Guess is null";
        }

        return {
            "folder": this.folder,
            "path": this.path,
            "name": this.name,
            "links": [this.guess]
        };
    }

    static _equals(a1: any[], a2: any[]) : boolean {
        if (a1.length != a2.length) {
            return false;
        }

        for (let i = 0; i < a1.length; i++) {
            if (a1[i] !== a2[i]) {
                return false;
            }
        }

        return true;
    }
}
