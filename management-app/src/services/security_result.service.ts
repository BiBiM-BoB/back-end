import { Model, ObjectId } from 'mongoose';
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';

import { SecurityResult, SecurityResultDocument } from '../models/schemas/security_result.schema';
import { CreateSecurityResultDto } from '../models/dto/security_result.dto'

@Injectable()
export class SecurityResultService {
  constructor(@InjectModel(SecurityResult.name) private securityResultModel: Model<SecurityResultDocument>) {}

  async create(createSecurityResultDto: CreateSecurityResultDto): Promise<SecurityResult> {
    const createdSecuityResult = new this.securityResultModel(createSecurityResultDto);
    return createdSecuityResult.save();
  }

  async findAll(): Promise<SecurityResult[]> {
    return this.securityResultModel.find().exec();
  }

  async find(id: string): Promise<SecurityResult> {
    return this.securityResultModel.findOne({ "_id": id });
  }
}