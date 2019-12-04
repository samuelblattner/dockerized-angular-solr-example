export class Document {
  public topic: string = '';
  public text: string = '';
  public summary: string = '';
  public nNouns: number = 0;
  public nVerbs: number = 0;
  public nDates: number = 0;

  public highlights: string[] = [];
}
