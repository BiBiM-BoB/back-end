import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type SecurityResultDocument = SecurityResult & Document;

@Schema()
export class SecurityResult {
  @Prop()
  data: string;
}

export const SecurityResultSchema = SchemaFactory.createForClass(SecurityResult);