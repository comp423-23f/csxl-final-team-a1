import { RxObject } from '../rx-object';
import EquipmentItem from './equipment-item.model';

export class RxItem extends RxObject<EquipmentItem[]> {
  pushItem(item: EquipmentItem): void {
    this.value.push(item);
    this.notify();
  }

  updateItem(item: EquipmentItem): void {
    this.value = this.value.map((o) => {
      return o.id !== item.id ? o : item;
    });
    this.notify();
  }

  removeItem(removeItem: EquipmentItem): void {
    this.value = this.value.filter(
      (item) => item.id != removeItem.id
    );
    this.notify();
  }
}