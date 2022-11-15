import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, now } from 'mongoose';

export type SecurityResultDocument = SecurityResult & Document;

@Schema()
export class SecurityResult {

  @Prop()
  pipelineName: string;

  @Prop()
  stage: string;

  @Prop()
  tool: string;

  @Prop({ default: now() })
  createdAt: Date;

  @Prop({ default: now() })
  updatedAt: Date;

  @Prop()
  data: [
    message: { text: string },
    locations: [
      { 
        physicalLocation: {
          artifactLocation: {
            uri: string,
            uriBaseId: string,
            index: number
          },
          region:{
            startLine: number,
            startColumn: number,
            endColumn: number
          }
        }
      }
    ],
    description: {
      id: string,
      name: string,
      shortDescription: {
        text: string
      },
      fullDescription: {
        text: string
      },
      defaultConfiguration: {
        enabled: boolean,
        level: string
      },
      properties: {
        tags: [],
        description: string,
        id: string,
        kind: string,
        precision: string,
        "problem.severity": string,
        "security-severity": string,
      }
    }
  ];
}

export const SecurityResultSchema = SchemaFactory.createForClass(SecurityResult);