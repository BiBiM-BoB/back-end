import { IsJSON, IsNotEmpty, IsNumber, IsObject, IsString, MaxLength } from "class-validator";
export class CreateSecurityResultDto {

    @IsString()
    readonly pipelineName: string;

    @IsNotEmpty()
    @IsString()
    readonly stage: string;
    
    @IsNotEmpty()
    @IsString()
    readonly tool: string;

    @IsNotEmpty()
    readonly createAt: Date;

    @IsNotEmpty()
    readonly updateAt: Date;
    
    @IsNotEmpty()
    readonly data: object;
}