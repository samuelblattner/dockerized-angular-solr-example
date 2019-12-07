export class Document {
  public topic: string = '';
  public text: string = '';
  public text_length: number = 0;
  public summary: string = '';
  public nNouns: number = 0;
  public nVerbs: number = 0;
  public nDates: number = 0;
  public score: number = 0;

  public highlights: string[] = [];
}
