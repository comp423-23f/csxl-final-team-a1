export default interface EquipmentType {
    id: number | null;
    title: string;
    num_available: Number;
    img_url: string;
    description: string;
    max_reservation_time: Number;
}