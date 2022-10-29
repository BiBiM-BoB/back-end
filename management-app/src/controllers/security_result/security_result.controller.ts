import { Body, Controller, Delete, Get, HttpStatus, Param, Post, Put, Res } from '@nestjs/common';

import { CreateSecurityResultDto } from '../../models/dto/security_result.dto';
import { SecurityResultService } from '../../services/security_result.service';

@Controller('security_result')
export class SecurityResultController {
  constructor(private readonly securityResultService: SecurityResultService) {}

  @Get(":id")
  getSecurityResult(@Param('id') id: string) {
    return this.securityResultService.find(id);
  }

  @Post("/createSecurityResult")
  saveSecurityResult(@Res() response, @Body() createSecurityResultDto: CreateSecurityResultDto) {
    const test = this.securityResultService.create(createSecurityResultDto);
    return response.status(HttpStatus.CREATED).json( {test} );
  }
}