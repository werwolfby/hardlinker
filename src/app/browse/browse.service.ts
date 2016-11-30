import { Injectable }      from '@angular/core';
import { Http }            from '@angular/http';
import { URLSearchParams } from '@angular/http';
import { Observable }      from "rxjs"
import "rxjs/add/operator/map";

export interface FileInfo {
    folder: string;
    path: string[];
    name: string;
}

export interface LinkInfo extends FileInfo {
    links: FileInfo[];
}

const LINKS_API_PATH = 'api/links';

@Injectable()
export class BrowseService {
    constructor (private _http: Http) {        
    }

    getAll() : Observable<LinkInfo[]> {
        return this._http
            .get(LINKS_API_PATH)
            .map(r => <LinkInfo[]> r.json());
    }

    link(src : FileInfo, dest : FileInfo) : Observable<LinkInfo> {
        let params : URLSearchParams = new URLSearchParams();
        params.set('folder', src.folder);
        params.set('path', [...src.path, src.name].join('/'));
        
        return this._http
            .post(LINKS_API_PATH, JSON.stringify(dest), { search: params })
            .map(r => {
                var result = <LinkInfo> r.json();
                result.links = [dest];
                return result;
            });
    }
}
