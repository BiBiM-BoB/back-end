import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type SecurityResultDocument = SecurityResult & Document;

@Schema()
export class SecurityResult {
  @Prop()
  name: string;

  @Prop()
  age: number;

  @Prop()
  location: string;
}

export const SecurityResultSchema = SchemaFactory.createForClass(SecurityResult);