import { Component } from '@angular/core';

@Component({
    selector: 'hl-links-table',
    template: `
    <table class="table table-striped">
        <tr>
            <th width="50%">Source</th>
            <th width="50%">Dest</th>
        </tr>
        <tr>
            <td width="50%">Src</td>
            <td width="50%">Dst</td>
        </tr>
    </table>
    `,
})
export class LinksTableComponent {
}