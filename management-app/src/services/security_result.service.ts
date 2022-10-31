import { Model, ObjectId } from 'mongoose';
import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';

import { SecurityResult, SecurityResultDocument } from '../models/schemas/security_result.schema';
import { CreateSecurityResultDto } from '../models/dto/security_result.dto';

@Injectable()
export class SecurityResultService {
  constructor(@InjectModel(SecurityResult.name) private securityResultModel: Model<SecurityResultDocument>) {}

  async create(createSecurityResultDto: CreateSecurityResultDto): Promise<SecurityResult> {

    if(createSecurityResultDto.data[0].message === undefined){ // 예외처리 방법 예시
      throw new BadRequestException();
    }

    const createdSecuityResult = await new this.securityResultModel(createSecurityResultDto);
    return await createdSecuityResult.save();
  }

  async findAll(): Promise<SecurityResult[]> {
    return this.securityResultModel.find().exec();
  }

  async find(id: string): Promise<SecurityResult> {
    return this.securityResultModel.findOne({ "_id": id });
  }
}